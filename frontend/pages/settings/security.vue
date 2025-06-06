<script setup lang="ts">
import PasswordChangeForm from '~/components/partials/settings/PasswordChangeForm.vue'
import EmailChangeForm from '~/components/partials/settings/EmailChangeForm.vue'

useHead({
    title: 'Security Settings',
})

interface Item {
    label: string
    value?: string
    action: () => void
}

definePageMeta({
    requiresAuth: true,
})

const authStore = useAuthStore()
const toastStore = useToastStore()
const isSendingVerificationLink = ref(false)
const isEmailChangeDialog = ref(false)
const isPasswordChangeDialog = ref(false)

const items = computed<Item[]>(() => [
    {label: 'Email', value: hiddenEmail.value, action: () => isEmailChangeDialog.value = true},
    {label: 'Change password', action: () => isPasswordChangeDialog.value = true},
])

const hiddenEmail = computed(() => {
    const email = authStore.email
    if (!email) return ''

    const atIndex = email.indexOf('@')
    const usernamePart = email.substring(0, Math.min(2, atIndex))
    const domainPart = email.substring(atIndex)

    return usernamePart + '***' + domainPart
})

async function sendVerificationLink() {
    isSendingVerificationLink.value = true

    try {
        await $api('/email/verify/', {
            method: 'POST',
            watch: false
        })

        toastStore.success('Verification link has been sent on your Email.')
    } catch (error: any) {
        if (error?.data && error.data.detail) {
            toastStore.error(error.data.detail)
        } else {
            toastStore.error('Unknown error occurred')
        }
    } finally {
        isSendingVerificationLink.value = false
    }
}
</script>

<template>
    <div>
        <h2 class="max-sm:hidden text-xl mb-4 font-semibold">Security Settings</h2>

        <v-alert
            v-if="!authStore.isEmailVerified"
            type="warning"
            variant="tonal"
            class="mb-2"
        >
            <p>Your email has not been verified yet!</p>
            <v-btn
                variant="outlined"
                class="normal-case mt-2 cursor-pointer"
                :loading="isSendingVerificationLink"
                @click="sendVerificationLink"
            >
                Resend the verification link
            </v-btn>
        </v-alert>

        <div class="rounded-lg border overflow-hidden">
            <v-btn
                v-for="item in items"
                variant="flat"
                append-icon="mdi-chevron-right"
                class="flex w-full not-last:border-b rounded-none normal-case justify-between cursor-pointer h-15"
                @click="item.action()"
            >
                <div class="text-start">
                    <p class="font-semibold">{{ item.label }}</p>
                    <p v-if="item.value" class="opacity-70">{{ item.value }}</p>
                </div>
            </v-btn>
        </div>

        <Dialog v-model="isEmailChangeDialog">
            <EmailChangeForm @submit="isEmailChangeDialog = false"/>
        </Dialog>
        <Dialog v-model="isPasswordChangeDialog">
            <PasswordChangeForm @submit="isPasswordChangeDialog = false"/>
        </Dialog>
    </div>
</template>

<style scoped>

</style>
