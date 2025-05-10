<script setup lang="ts">
import 'vuetify/components'
import AuthDialog from '~/components/partials/auth/AuthDialog.vue'
import LogOutDialog from '~/components/partials/auth/LogOutDialog.vue'

const modalStore = useModalStore()
</script>

<template>
    <AuthDialog v-model="modalStore.authModal"/>
    <LogOutDialog v-model="modalStore.logoutModal"/>
</template>

<style scoped>

</style>
