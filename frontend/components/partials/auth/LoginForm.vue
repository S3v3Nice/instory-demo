<script setup lang="ts">
import 'vuetify/components'
import {useThemeStore} from '~/stores/theme'
import {useAuthStore} from '~/stores/auth'
import {useToastStore} from '~/stores/toast'

const emit = defineEmits(['switch-to-register', 'switch-to-forgot-password'])

const authStore = useAuthStore()
const themeStore = useThemeStore()
const toastStore = useToastStore()

const isLoading = ref(false)

const data = reactive({
    username: '',
    password: '',
    remember_me: true
})
const errors = ref<{ [key: string]: string[] }>({})

async function submitLogin() {
    errors.value = {}
    isLoading.value = true

    try {
        await $api('/auth/login/', {
            method: 'POST',
            body: data,
            watch: false
        })

        await authStore.fetchUser()

        toastStore.success('You have successfully logged in!')
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
        isLoading.value = false
    }
}
</script>

<template>
    <div>
        <div class="flex flex-col items-center gap-2 mb-7 px-4">
            <img
                :src="themeStore.isDark ? '/logo-min-dark.svg' : '/logo-min.svg'"
                alt="Logo"
                class="w-[50px]"
            >

            <p class="text-3xl font-semibold">Welcome back!</p>
            <p class="text-lg">Log into your account</p>
        </div>

        <v-form @submit.prevent="submitLogin">
            <v-container>
                <v-text-field
                    v-model="data.username"
                    label="Email or username"
                    variant="outlined"
                    :error-messages="errors['username']"
                />
                <v-text-field
                    v-model="data.password"
                    type="password"
                    label="Password"
                    variant="outlined"
                    :error-messages="errors['password']"
                    class="mt-2"
                />

                <div class="flex items-center justify-between">
                    <v-checkbox
                        v-model="data.remember_me"
                        hide-details="auto"
                        class="-ml-2 text-xs"
                    >
                        <template v-slot:label>
                            <span class="max-sm:text-sm">Remember me</span>
                        </template>
                    </v-checkbox>
                    <v-btn
                        variant="text"
                        class="cursor-pointer text-none -mr-4 max-sm:text-sm"
                        @click="emit('switch-to-forgot-password')"
                    >
                        Forgot password?
                    </v-btn>
                </div>

                <v-btn
                    color="primary"
                    block
                    class="cursor-pointer mt-4"
                    :loading="isLoading"
                    type="submit"
                >
                    Log in
                </v-btn>

                <v-btn
                    block
                    variant="text"
                    class="cursor-pointer text-none mt-1"
                    @click="emit('switch-to-register')"
                >
                    Don't have an account?
                </v-btn>
            </v-container>
        </v-form>
    </div>
</template>

<style scoped>

</style>
