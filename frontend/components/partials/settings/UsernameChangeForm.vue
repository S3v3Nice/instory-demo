<script setup lang="ts">
const emit = defineEmits(['submit'])
const authStore = useAuthStore()
const toastStore = useToastStore()
const errors = ref<{ [key: string]: string[] }>({})
const username = ref(authStore.username!)
const isSubmitting = ref(false)

const isChanged = computed(() => username.value !== authStore.username)

async function submit() {
    errors.value = {}
    isSubmitting.value = true

    try {
        await $api('/settings/profile/username/', {
            method: 'PUT',
            body: {username: username.value},
            watch: false
        })

        authStore.user!.username = username.value
        emit('submit')
        toastStore.success('Username has been successfully changed.')
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
    <div class="px-4 mb-8">
        <p class="text-xl font-semibold mb-2">Change username</p>
        <p class="text-sm">
            Username is your primary display name across the platform. It is used to log into your account.
            When you change username, the profile link also changes.
        </p>
    </div>

    <v-form @submit.prevent="submit">
        <v-container class="pt-0">
            <v-text-field
                v-model="username"
                label="Username"
                variant="outlined"
                :readonly="isSubmitting"
                :error-messages="errors['username']"
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
</template>

<style scoped>

</style>
