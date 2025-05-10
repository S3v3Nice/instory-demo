export default defineNuxtPlugin(async () => {
    const authStore = useAuthStore()
    if (!authStore.isFetched) {
        await authStore.fetchInitialUser()
    }
})
