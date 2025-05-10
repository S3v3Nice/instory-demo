<script setup lang="ts">
const isOpen = defineModel<boolean>({required: true})

const toastStore = useToastStore()
const errors = ref<{ [key: string]: string[] }>({})
const data = reactive({
    old_password: '',
    new_password1: '',
    new_password2: '',
})
const isSubmitting = ref(false)

watch(isOpen, (isOpen) => {
    if (!isOpen) {
        data.old_password = ''
        data.new_password1 = ''
        data.new_password2 = ''
    }
})

async function submit() {
    errors.value = {}
    isSubmitting.value = true

    try {
        await $api('/password/', {
            method: 'PUT',
            body: data,
            watch: false
        })

        isOpen.value = false
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
    <v-dialog v-model="isOpen" max-width="600">
        <template v-slot:default="{ isActive }">
            <v-card>
                <v-card-title class="w-full flex items-center pb-0">
                    <v-btn icon flat class="cursor-pointer ml-auto" @click="isActive.value = false">
                        <v-icon>mdi-close</v-icon>
                    </v-btn>
                </v-card-title>

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
                        />

                        <v-text-field
                            v-model="data.new_password1"
                            label="New password"
                            variant="outlined"
                            :readonly="isSubmitting"
                            :error-messages="errors['new_password1']"
                            type="password"
                        />

                        <v-text-field
                            v-model="data.new_password2"
                            label="Repeat new password"
                            variant="outlined"
                            :readonly="isSubmitting"
                            :error-messages="errors['new_password2']"
                            type="password"
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
            </v-card>
        </template>
    </v-dialog>
</template>

<style scoped>

</style>
