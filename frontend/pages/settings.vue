<script setup lang="ts">
import SettingsMenu from '~/components/partials/settings/SettingsMenu.vue'

useHead({
    title: 'Settings',
})

const route = useRoute()

const isNested = computed(() => {
    const matchedCount = route.matched.length
    return matchedCount > 1
})
</script>

<template>
    <div v-if="isNested" class="flex h-screen">
        <div class="flex flex-1">
            <div class="w-[315px] h-full overflow-auto border-r p-4 max-sm:hidden">
                <p class="p-4 text-xl font-semibold">Settings</p>
                <SettingsMenu/>
            </div>

            <div class="flex-1 overflow-auto p-4 flex justify-center">
                <div class="w-full max-w-[706px]">
                    <NuxtPage/>
                </div>
            </div>
        </div>
    </div>

    <div v-else class="p-4">
        <SettingsMenu/>
    </div>
</template>

<style scoped>

</style>
