<script setup lang="ts">
import 'vuetify/components'
import LoginForm from '~/components/partials/auth/LoginForm.vue'
import RegisterForm from '~/components/partials/auth/RegisterForm.vue'
import ForgotPasswordForm from '~/components/partials/auth/ForgotPasswordForm.vue'

enum FormType {
    Login,
    Register,
    ForgotPassword
}

const formType = ref<FormType>(FormType.Login)
const isDialogOpen = ref(false)

watch(isDialogOpen, (openDialog) => {
    if (openDialog) {
        formType.value = FormType.Login
    }
})
</script>

<template>
    <v-dialog v-model="isDialogOpen" max-width="500">
        <template v-slot:activator="{ props: activatorProps }">
            <slot name="activator" :props="activatorProps"/>
        </template>

        <template v-slot:default="{ isActive }">
            <v-card>
                <v-card-title class="w-full flex items-center">
                    <v-btn icon flat class="cursor-pointer ml-auto" @click="isActive.value = false">
                        <v-icon>mdi-close</v-icon>
                    </v-btn>
                </v-card-title>

                <LoginForm
                    v-if="formType === FormType.Login"
                    @switch-to-register="formType = FormType.Register"
                    @switch-to-forgot-password="formType = FormType.ForgotPassword"
                />
                <RegisterForm
                    v-else-if="formType === FormType.Register"
                    @switch-to-login="formType = FormType.Login"
                />
                <ForgotPasswordForm
                    v-else-if="formType === FormType.ForgotPassword"
                    @switch-to-login="formType = FormType.Login"
                />
            </v-card>
        </template>
    </v-dialog>
</template>

<style scoped>

</style>
