<script setup>
import NavBar from '~/components/partials/NavBar.vue'
import MobileNavBar from '~/components/partials/MobileNavBar.vue'
import GlobalToasts from '~/components/partials/GlobalToasts.vue'
import GlobalModals from '~/components/partials/GlobalModals.vue'
import AuthRequired from '~/components/partials/pageAccessErrors/AuthRequired.vue'

const pageAccessErrorStore = usePageAccessErrorStore()
</script>

<template>
    <NuxtLayout>
        <v-app>
            <GlobalToasts/>
            <GlobalModals/>
            <NavBar class="max-sm:hidden"/>
            <MobileNavBar class="sm:hidden"/>
            <div
                class="page max-sm:mb-[var(--nav-mobile-height)] sm:ml-[var(--nav-narrow-width)]
                       xl:ml-[var(--nav-medium-width)] 2xl:ml-[var(--nav-wide-width)]"
            >
                <AuthRequired v-if="pageAccessErrorStore.authRequired"/>
                <NuxtPage v-else/>
            </div>
        </v-app>
    </NuxtLayout>
</template>

<style scoped>

</style>
