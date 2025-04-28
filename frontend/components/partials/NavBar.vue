<script setup lang="ts">
import 'vuetify/components'
import AuthDialog from '~/components/partials/auth/AuthDialog.vue'

interface Item {
    label: string
    icon: string
    visible?: boolean
}

interface ExtraMenuItem {
    label: string
    icon: string
    visible?: boolean
    switchValue?: boolean
    action?: () => void
}

const authStore = useAuthStore()
const themeStore = useThemeStore()
const toastStore = useToastStore()

const isMenuOpen = ref(false)
const isLogOutDialog = ref(false)
const isLoggingOut = ref(false)
const items = computed<Item[]>(() => [
    {label: 'Home', icon: 'mdi-home-outline'},
    {label: 'Search', icon: 'mdi-magnify'},
    {label: 'Explore', icon: 'mdi-compass-outline'},
    {label: 'Create', icon: 'mdi-plus-box-outline'},
    {label: 'Profile', icon: 'mdi-account-circle', visible: authStore.isAuthenticated},
])
const extraItems = computed<ExtraMenuItem[]>(() => [
    {
        label: 'Settings',
        icon: 'mdi-cog-outline',
        visible: true
    },
    {
        label: 'Switch theme',
        icon: themeStore.isDark ? 'mdi-weather-night' : 'mdi-weather-sunny',
        switchValue: themeStore.isDark,
        action: themeStore.toggleTheme
    },
    {
        label: 'Log out',
        icon: 'mdi-logout',
        action: () => isLogOutDialog.value = true,
        visible: authStore.isAuthenticated
    },
])

function onMenuItemClick(item: ExtraMenuItem) {
    if (item.action !== undefined) {
        item.action()
    }

    if (item.switchValue === undefined) {
        isMenuOpen.value = false
    }
}

async function logout() {
    isLoggingOut.value = true

    try {
        await $api('/auth/logout/', {
            method: 'POST',
            watch: false
        })

        isLogOutDialog.value = false

        authStore.reset()

        toastStore.success('You have successfully logged out!')
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
    <nav>
        <div
            class="flex flex-col fixed w-[var(--nav-narrow-width)] xl:w-[var(--nav-medium-width)]
                   2xl:w-[var(--nav-wide-width)] px-2 py-7 border-r mr-5 h-full"
        >
            <NuxtLink :to="{name: 'index'}" class="h-[32px] px-4">
                <template v-if="themeStore.isDark">
                    <img src="/logo-dark.svg" alt="Logo" class="h-full max-xl:hidden">
                    <img src="/logo-min-dark.svg" alt="Logo" class="h-full block xl:hidden">
                </template>
                <template v-else>
                    <img src="/logo.svg" alt="Logo" class="h-full max-xl:hidden">
                    <img src="/logo-min.svg" alt="Logo" class="h-full block xl:hidden">
                </template>
            </NuxtLink>

            <div class="flex flex-col gap-1 mt-7">
                <template v-for="item in items">
                    <v-btn
                        v-if="item.visible !== false"
                        variant="text"
                        class="flex xl:justify-start text-none cursor-pointer h-12 max-xl:px-0 min-w-0"
                    >
                        <div class="flex gap-4 items-center">
                            <v-icon :icon="item.icon" size="24"/>
                            <span class="max-xl:hidden">{{ item.label }}</span>
                        </div>
                    </v-btn>
                </template>
            </div>

            <v-menu v-model="isMenuOpen" :close-on-content-click="false">
                <template v-slot:activator="{ props }">
                    <div class="mt-auto w-full">
                        <div class="sticky left-0 bottom-0 w-full">
                            <v-btn
                                v-bind="props"
                                variant="text"
                                class="flex xl:justify-start text-none cursor-pointer h-12 max-xl:px-0 min-w-0 w-full"
                            >
                                <div class="flex gap-4 items-center">
                                    <v-icon icon="mdi-menu" size="24"/>
                                    <span class="max-xl:hidden">More</span>
                                </div>
                            </v-btn>
                        </div>
                    </div>
                </template>

                <v-list>
                    <v-list-item v-for="(item, i) in extraItems" :key="i" :value="i" @click="onMenuItemClick(item)">
                        <template v-slot:prepend>
                            <v-icon :icon="item.icon"></v-icon>
                        </template>

                        <v-list-item-title>{{ item.label }}</v-list-item-title>
                    </v-list-item>
                </v-list>
            </v-menu>

            <AuthDialog v-if="!authStore.isAuthenticated">
                <template #activator="{props: activatorProps}">
                    <v-btn
                        v-bind="activatorProps"
                        color="primary"
                        variant="flat"
                        class="flex xl:justify-start text-none cursor-pointer h-12 mt-2 max-xl:px-0 min-w-0 w-full"
                    >
                        <div class="flex gap-4 items-center">
                            <v-icon icon="mdi-login" size="24"/>
                            <span class="max-xl:hidden">Log in</span>
                        </div>
                    </v-btn>
                </template>
            </AuthDialog>

            <v-dialog v-model="isLogOutDialog" max-width="500">
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
                            <v-btn text="No" class="cursor-pointer" @click="isLogOutDialog = false"/>
                            <v-btn
                                text="Yes"
                                variant="flat"
                                color="surface-variant"
                                class="cursor-pointer"
                                @click="logout"
                            />
                        </v-card-actions>
                    </v-card>
                </template>
            </v-dialog>
        </div>
    </nav>
</template>

<style scoped>

</style>
