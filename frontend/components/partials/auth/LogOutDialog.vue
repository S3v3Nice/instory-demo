<script setup lang="ts">
import ConfirmationDialog from '~/components/ConfirmationDialog.vue'

const toastStore = useToastStore()
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
    <ConfirmationDialog
        title="Log out?"
        description="Are you sure you want to log out of your account?"
        cancel-btn="Cancel"
        confirm-btn="Log out"
        @confirm="logout"
    />
</template>

<style scoped>

</style>
