<script setup lang="ts">
const modalStore = useModalStore()
onMounted(() => {
    modalStore.authModal = true
})
</script>

<template>
    <div class="flex flex-col items-center justify-center min-h-screen text-center px-4">
        <div class="p-6 max-w-md w-full flex flex-col items-center gap-2">
            <v-icon size="64" color="error">mdi-hand-back-left-outline</v-icon>
            <p class="text-2xl font-semibold">Authorization required</p>
            <p class="opacity-80">
                This page is available only to authenticated users.
            </p>
            <v-btn
                color="primary"
                variant="tonal"
                @click="modalStore.authModal = true"
                class="mt-6 w-full cursor-pointer"
            >
                Log in
            </v-btn>
        </div>
    </div>
</template>

<style scoped>

</style>
