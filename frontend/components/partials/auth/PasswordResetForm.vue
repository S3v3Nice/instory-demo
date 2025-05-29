<script setup lang="ts">
import 'vuetify/components'
import {useThemeStore} from '~/stores/theme'
import {useToastStore} from '~/stores/toast'

const emit = defineEmits(['switch-to-login'])

const themeStore = useThemeStore()
const toastStore = useToastStore()

const isLoading = ref(false)

const data = reactive({
    email: ''
})
const errors = ref<{ [key: string]: string[] }>({})

async function submit() {
    errors.value = {}
    isLoading.value = true

    $api('/password/reset/', {
        method: 'POST',
        body: data,
        watch: false
    }).then(() => {
        toastStore.success('We\'ve sent a password reset link to the email provided!')
    }).catch((error) => {
        if (error?.data) {
            errors.value = error.data
            if (error.data.__all__) {
                toastStore.error(error.data.__all__[0])
            }
        } else {
            toastStore.error('Unknown error occurred')
        }
    }).finally(() => {
        isLoading.value = false
    })
}
</script>

<template>
    <div>
        <div class="flex flex-col items-center gap-4 mb-7 px-4">
            <img
                :src="themeStore.isDark ? '/logo-min-dark.svg' : '/logo-min.svg'"
                alt="Logo"
                class="w-[50px]"
            >

            <p class="text-3xl font-semibold">Password Reset</p>
            <p class="">Enter your email and we will send you a password reset link.</p>
        </div>

        <v-form @submit.prevent="submit">
            <v-container>
                <v-text-field
                    v-model="data.email"
                    label="Email"
                    :error-messages="errors['email']"
                    variant="outlined"
                />

                <v-btn
                    color="primary"
                    block
                    class="cursor-pointer mt-4"
                    :loading="isLoading"
                    type="submit"
                >
                    Send link
                </v-btn>

                <v-btn
                    block
                    variant="text"
                    class="cursor-pointer normal-case mt-1"
                    @click="emit('switch-to-login')"
                >
                    Remember password?
                </v-btn>
            </v-container>
        </v-form>
    </div>
</template>

<style scoped>

</style>
