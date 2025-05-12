<script setup lang="ts">
const emit = defineEmits(['submit'])
const toastStore = useToastStore()
const errors = ref<{ [key: string]: string[] }>({})
const data = reactive({
    old_password: '',
    new_password1: '',
    new_password2: '',
})
const isSubmitting = ref(false)

async function submit() {
    errors.value = {}
    isSubmitting.value = true

    try {
        await $api('/settings/security/password/', {
            method: 'PUT',
            body: data,
            watch: false
        })

        emit('submit')
        toastStore.success('Password has been successfully changed.')
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
        <p class="text-xl font-semibold mb-2">Change password</p>
        <p class="text-sm">
            Password is used to log in to your account. Here you can change your password.
        </p>
    </div>

    <v-form @submit.prevent="submit">
        <v-container class="pt-0 flex flex-col gap-3">
            <v-text-field
                v-model="data.old_password"
                label="Old password"
                variant="outlined"
                :readonly="isSubmitting"
                :error-messages="errors['old_password']"
                type="password"
                class="mb-2"
            />

            <v-text-field
                v-model="data.new_password1"
                label="New password"
                variant="outlined"
                :readonly="isSubmitting"
                :error-messages="errors['new_password1']"
                type="password"
                class="mb-2"
            />

            <v-text-field
                v-model="data.new_password2"
                label="Repeat new password"
                variant="outlined"
                :readonly="isSubmitting"
                :error-messages="errors['new_password2']"
                type="password"
                class="mb-2"
            />

            <v-btn
                color="primary"
                variant="flat"
                :disabled="!data.old_password || !data.new_password1 || !data.new_password2"
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
