<script setup lang="ts">
import 'vuetify/components'
import {useToastStore} from '~/stores/toast'

const toastStore = useToastStore()
</script>

<template>
    <v-snackbar-queue v-model="toastStore.errors" color="error" position="absolute"/>
    <v-snackbar-queue v-model="toastStore.successes" color="success" position="absolute"/>
</template>

<style scoped>

</style>
