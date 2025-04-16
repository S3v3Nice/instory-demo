<script setup lang="ts">
import {useTheme} from 'vuetify'
import 'vuetify/components'

interface Item {
    icon: string
    visible?: boolean
    action?: () => void
}

const theme = useTheme()
const items = computed<Item[]>(() => [
    {icon: 'mdi-home-outline'},
    {icon: 'mdi-magnify'},
    {icon: 'mdi-compass-outline'},
    {icon: 'mdi-plus-box-outline'},
    {icon: 'mdi-account-circle', visible: true},
])
</script>

<template>
    <v-bottom-navigation>
        <v-btn v-for="item in items">
            <v-icon size="large">{{ item.icon }}</v-icon>
        </v-btn>
    </v-bottom-navigation>
</template>

<style scoped>

</style>
