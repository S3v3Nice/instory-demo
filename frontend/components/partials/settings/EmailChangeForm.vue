<script setup lang="ts">
const emit = defineEmits(['submit'])
const authStore = useAuthStore()
const toastStore = useToastStore()
const errors = ref<{ [key: string]: string[] }>({})
const email = ref(authStore.email!)
const isSubmitting = ref(false)

const isChanged = computed(() => email.value !== authStore.email)

async function submit() {
    errors.value = {}
    isSubmitting.value = true

    try {
        await $api('/settings/security/email/', {
            method: 'PUT',
            body: {email: email.value},
            watch: false
        })

        authStore.user!.email = email.value
        authStore.user!.date_verified_email = null
        emit('submit')
        toastStore.success('Email has been successfully changed.')
    } catch (error: any) {
        if (error?.data) {
            errors.value = error.data
            if (error.data.__all__) {
                toastStore.error(error.data.__all__[0])
            }
        } else {
            toastStore.error('Unknown error occurred')
        }
    } finally {
        isSubmitting.value = false
    }
}
</script>

<template>
    <div>
        <div class="px-4 mb-8">
            <p class="text-xl font-semibold mb-2">Email</p>
            <p class="text-sm">Email is used to identify you, log in to your account, receive
                notifications, and recover access if you forget your password. Here you can change your
                email.</p>
        </div>

        <v-form @submit.prevent="submit">
            <v-container class="pt-0">
                <v-text-field
                    v-model="email"
                    label="Email"
                    variant="outlined"
                    :readonly="isSubmitting"
                    :error-messages="errors['email']"
                    class="mb-2"
                />

                <v-btn
                    color="primary"
                    variant="flat"
                    :disabled="!isChanged"
                    :loading="isSubmitting"
                    type="submit"
                    class="w-full cursor-pointer"
                >
                    Save
                </v-btn>
            </v-container>
        </v-form>
    </div>
</template>

<style scoped>

</style>
