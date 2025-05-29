<script setup lang="ts">

interface Item {
    label: string
    icon?: string
    routeName?: string
    action?: () => void
    class?: string
    danger?: boolean
    visible?: boolean
}

const route = useRoute()
const authStore = useAuthStore()
const modalStore = useModalStore()

const items = computed<Item[]>(() => [
    {
        label: 'Profile',
        icon: 'mdi-account-circle-outline',
        routeName: 'settings-profile',
        visible: authStore.isAuthenticated
    },
    {label: 'Security', icon: 'mdi-lock-outline', routeName: 'settings-security', visible: authStore.isAuthenticated},
    {label: 'Theme', icon: 'mdi-weather-sunny', routeName: 'settings-theme', class: 'sm:hidden'},
    {
        label: 'Log out',
        class: 'sm:hidden',
        danger: true,
        visible: authStore.isAuthenticated,
        action: () => modalStore.logoutModal = true
    },
])

function onItemClick(item: Item) {
    if (item.action) {
        item.action()
    }
}
</script>

<template>
    <div>
        <template v-for="(item, i) in items" :key="i">
            <component
                v-if="item.visible !== false"
                :is="item.routeName ? 'RouterLink' : 'div'"
                :to="{name: item.routeName}"
                :class="item.class"
                @click="onItemClick(item)"
            >
                <v-btn
                    variant="text"
                    :active="route.name === item.routeName"
                    :color="item.danger ? 'error' : undefined"
                    class="flex justify-start normal-case cursor-pointer h-12 min-w-0 w-full"
                >
                    <div class="flex gap-4 items-center">
                        <v-icon v-if="item.icon" :icon="item.icon" size="24"/>
                        <span>{{ item.label }}</span>
                    </div>
                </v-btn>
            </component>
        </template>
    </div>
</template>

<style scoped>

</style>
