<script setup lang="ts">
import 'vuetify/components'
import type {RouteLocationRaw} from '#vue-router'

interface Item {
    label: string
    icon?: string
    route?: RouteLocationRaw
    action?: () => void
    visible?: boolean
    avatar?: boolean
}

interface ExtraMenuItem {
    label: string
    icon: string
    visible?: boolean
    switchValue?: boolean
    route?: RouteLocationRaw
    action?: () => void
}

const authStore = useAuthStore()
const themeStore = useThemeStore()
const modalStore = useModalStore()

const isMenuOpen = ref(false)
const items = computed<Item[]>(() => [
    {label: 'Home', icon: 'mdi-home-outline', route: {name: 'index'}},
    {label: 'Search', icon: 'mdi-magnify'},
    {label: 'Explore', icon: 'mdi-compass-outline'},
    {label: 'Create', icon: 'mdi-plus-box-outline', action: () => modalStore.postCreateModal = true},
    {label: 'Profile', avatar: true, visible: authStore.isAuthenticated},
])
const extraItems = computed<ExtraMenuItem[]>(() => [
    {
        label: 'Settings',
        icon: 'mdi-cog-outline',
        route: {name: 'settings-profile'},
        visible: authStore.isAuthenticated
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
        action: () => modalStore.logoutModal = true,
        visible: authStore.isAuthenticated
    },
])

function onItemClick(item: Item) {
    if (item.action !== undefined) {
        item.action()
    }
}

function onMenuItemClick(item: ExtraMenuItem) {
    if (item.action !== undefined) {
        item.action()
    }

    if (item.switchValue === undefined) {
        isMenuOpen.value = false
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
                <template v-for="(item, i) in items" :key="i">
                    <component
                        v-if="item.visible !== false"
                        :is="item.route ? 'RouterLink' : 'div'"
                        :to="item.route"
                        @click="onItemClick(item)"
                    >
                        <v-btn
                            variant="text"
                            class="flex xl:justify-start text-none cursor-pointer h-12 max-xl:px-0 min-w-0 w-full"
                        >
                            <div class="flex gap-4 items-center">
                                <Avatar v-if="item.avatar" :user="authStore.user" :size="24"></Avatar>
                                <v-icon v-else-if="item.icon" :icon="item.icon" size="24"/>
                                <span class="max-xl:hidden">{{ item.label }}</span>
                            </div>
                        </v-btn>
                    </component>
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
                    <template v-for="(item, i) in extraItems" :key="i">
                        <component
                            v-if="item.visible !== false"
                            :is="item.route ? 'RouterLink' : 'div'"
                            :to="item.route"
                        >
                            <v-list-item :value="i" @click="onMenuItemClick(item)">
                                <template v-slot:prepend>
                                    <v-icon :icon="item.icon"></v-icon>
                                </template>

                                <v-list-item-title>{{ item.label }}</v-list-item-title>
                            </v-list-item>
                        </component>
                    </template>
                </v-list>
            </v-menu>

            <v-btn
                v-if="!authStore.isAuthenticated"
                color="primary"
                variant="flat"
                class="flex xl:justify-start text-none cursor-pointer h-12 mt-2 max-xl:px-0 min-w-0 w-full"
                @click="modalStore.authModal = true"
            >
                <div class="flex gap-4 items-center">
                    <v-icon icon="mdi-login" size="24"/>
                    <span class="max-xl:hidden">Log in</span>
                </div>
            </v-btn>
        </div>
    </nav>
</template>

<style scoped>

</style>
