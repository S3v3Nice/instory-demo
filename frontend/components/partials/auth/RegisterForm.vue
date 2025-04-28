<script setup lang="ts">
import 'vuetify/components'
import {useThemeStore} from '~/stores/theme'
import {useAuthStore} from '~/stores/auth'
import {useToastStore} from '~/stores/toast'

const emit = defineEmits(['switch-to-login'])

const authStore = useAuthStore()
const themeStore = useThemeStore()
const toastStore = useToastStore()

const isLoading = ref(false)

const data = reactive({
    email: '',
    username: '',
    password: '',
    password_confirm: ''
})
const errors = ref<{ [key: string]: string[] }>({})

async function submitRegister() {
    errors.value = {}
    isLoading.value = true

    try {
        await $api('/auth/register/', {
            method: 'POST',
            body: data,
            watch: false
        })

        await authStore.fetchUser()

        toastStore.success('You have successfully registered!')
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
    <div class="flex flex-col items-center gap-2 mb-7 px-4">
        <img
            :src="themeStore.isDark ? '/logo-min-dark.svg' : '/logo-min.svg'"
            alt="Logo"
            class="w-[50px]"
        >

        <p class="text-3xl font-semibold">Welcome!</p>
        <p class="text-lg">Create your account</p>
    </div>

    <v-form @submit.prevent="submitRegister">
        <v-container>
            <v-row>
                <v-col
                    cols="12"
                    sm="6"
                >
                    <v-text-field
                        v-model="data.email"
                        label="Email"
                        variant="outlined"
                        :error-messages="errors['email']"
                    ></v-text-field>
                </v-col>

                <v-col
                    cols="12"
                    sm="6"
                >
                    <v-text-field
                        v-model="data.username"
                        label="Username"
                        variant="outlined"
                        :error-messages="errors['username']"
                    ></v-text-field>
                </v-col>

                <v-col
                    cols="12"
                    sm="6"
                >
                    <v-text-field
                        v-model="data.password"
                        type="password"
                        label="Password"
                        variant="outlined"
                        :error-messages="errors['password']"
                    ></v-text-field>
                </v-col>

                <v-col
                    cols="12"
                    sm="6"
                >
                    <v-text-field
                        v-model="data.password_confirm"
                        type="password"
                        label="Repeat password"
                        variant="outlined"
                        :error-messages="errors['password_confirm']"
                    ></v-text-field>
                </v-col>
            </v-row>

            <v-btn
                color="primary"
                block
                class="cursor-pointer mt-4"
                :loading="isLoading"
                type="submit"
            >
                Register
            </v-btn>

            <v-btn
                block
                variant="text"
                class="cursor-pointer text-none mt-1"
                @click="emit('switch-to-login')"
            >
                Already have an account?
            </v-btn>
        </v-container>
    </v-form>
</template>

<style scoped>

</style>
