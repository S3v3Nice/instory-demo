<script setup lang="ts">
useHead({
    title: 'Theme Settings',
})

const themeStore = useThemeStore()
</script>

<template>
    <div>
        <h2 class="max-sm:hidden text-xl mb-4">Theme Settings</h2>
        <div class="border rounded-2xl px-4 flex justify-between items-center">
            <p>Dark theme</p>
            <v-switch
                :model-value="themeStore.isDark"
                inset
                hide-details
                @update:model-value="themeStore.toggleTheme()"
            />
        </div>
    </div>
</template>

<style scoped>

</style>
