export default defineNuxtRouteMiddleware((to) => {
    const authStore = useAuthStore()
    const pageAccessErrorStore = usePageAccessErrorStore()

    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        pageAccessErrorStore.authRequired = true
        return
    }

    pageAccessErrorStore.authRequired = false
})
