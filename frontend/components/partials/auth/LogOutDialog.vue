<script setup lang="ts">

const toastStore = useToastStore()
const authStore = useAuthStore()
const router = useRouter()

const isOpen = defineModel<boolean>({required: true})
const isLoggingOut = ref(false)

async function logout() {
    isLoggingOut.value = true

    try {
        await $api('/auth/logout/', {
            method: 'POST',
            watch: false
        })
        window.location.reload()
    } catch (error: any) {
        if (error?.data) {
            if (error.data.__all__) {
                toastStore.error(error.data.__all__[0])
            }
        } else {
            toastStore.error('Unknown error occurred')
        }
    } finally {
        isLoggingOut.value = false
    }
}
</script>

<template>
    <v-dialog v-model="isOpen" max-width="500">
        <template v-slot:default="{ isActive }">
            <v-card>
                <v-card-title class="w-full flex items-center">
                    <span>Logging out</span>
                    <v-btn icon flat class="cursor-pointer ml-auto" @click="isActive.value = false">
                        <v-icon>mdi-close</v-icon>
                    </v-btn>
                </v-card-title>

                <v-card-text>
                    Do you really want to log out?
                </v-card-text>

                <v-card-actions>
                    <v-btn text="No" class="cursor-pointer" @click="isOpen = false"/>
                    <v-btn
                        text="Yes"
                        variant="flat"
                        :loading="isLoggingOut"
                        color="surface-variant"
                        class="cursor-pointer"
                        @click="logout"
                    />
                </v-card-actions>
            </v-card>
        </template>
    </v-dialog>
</template>

<style scoped>

</style>
