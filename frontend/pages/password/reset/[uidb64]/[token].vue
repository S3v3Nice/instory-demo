<script setup lang="ts">
useHead({
    title: 'Password Reset',
})

const route = useRoute()

const themeStore = useThemeStore()
const uidb64 = route.params.uidb64
const token = route.params.token
const isLoading = ref(false)
const isSuccess = ref(false)
const isError = ref(false)
const isInvalidToken = ref(false)
const errors = ref<{ [key: string]: string[] }>({})
const data = reactive({
    new_password1: '',
    new_password2: ''
})

async function submit() {
    isLoading.value = true
    isSuccess.value = false
    isError.value = false
    errors.value = {}

    try {
        await $api(`/password/reset/${uidb64}/${token}/`, {
            method: 'POST',
            body: data,
            watch: false
        })
        isSuccess.value = true
    } catch (error: any) {
        isError.value = true
        if (error?.data) {
            errors.value = error.data
            isInvalidToken.value = error.data.is_invalid_token
        }
    } finally {
        isLoading.value = false
    }
}
</script>

<template>
    <div class="flex justify-center h-[80vh] items-center">
        <div v-if="isInvalidToken || isSuccess">
            <div v-if="isInvalidToken" class="flex flex-col gap-2">
                <v-icon icon="mdi-alert-circle" size="64" color="error" class="self-center"/>
                <p class="text-2xl font-semibold text-center">Invalid token</p>
                <p class="opacity-80 text-center">Sorry, it looks like your password reset token is invalid.</p>
            </div>
            <div v-else-if="isSuccess" class="flex flex-col gap-2">
                <v-icon icon="mdi-check-circle" size="64" color="success" class="self-center"/>
                <p class="text-2xl font-semibold text-center">Password changed!</p>
                <p class="opacity-80 text-center">Your password has been successfully changed!</p>
            </div>
            <NuxtLink :to="{name: 'index'}">
                <v-btn
                    color="primary"
                    variant="tonal"
                    prepend-icon="mdi-home"
                    class="flex text-none cursor-pointer max-xl:px-0 min-w-0 w-full mt-6"
                >
                    Go Home
                </v-btn>
            </NuxtLink>
        </div>

        <v-form v-else @submit.prevent="submit" class="max-w-full">
            <v-container class="flex flex-col">
                <img
                    :src="themeStore.isDark ? '/logo-min-dark.svg' : '/logo-min.svg'"
                    alt="Logo"
                    class="w-[50px] self-center mb-2"
                >
                <p class="text-center text-2xl mb-2">Change your password</p>
                <p class="text-center opacity-80 mb-8">Enter a new password below to change your password.</p>

                <v-text-field
                    v-model="data.new_password1"
                    type="password"
                    label="New password"
                    variant="outlined"
                    :error-messages="errors['new_password1']"
                />
                <v-text-field
                    v-model="data.new_password2"
                    type="password"
                    label="Repeat new password"
                    variant="outlined"
                    :error-messages="errors['new_password2']"
                    class="mt-2"
                />

                <v-btn
                    color="primary"
                    block
                    :loading="isLoading"
                    type="submit"
                    class="cursor-pointer mt-4 w-[40rem] mb-4"
                >
                    Set new password
                </v-btn>

                <v-alert v-if="isError && Object.keys(errors).length === 0" type="error" variant="tonal" class="hidden">
                    Unknown error occurred.
                </v-alert>
            </v-container>
        </v-form>
    </div>
</template>

<style scoped>

</style>
