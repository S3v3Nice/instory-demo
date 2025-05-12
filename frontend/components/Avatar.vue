<script setup lang="ts">
import type {User} from '~/types'

defineProps({
    user: {
        type: Object as PropType<User | null>,
        required: true
    },
    size: {
        type: Number,
        default: '56'
    }
})
</script>

<template>
    <v-avatar v-if="user?.avatar" :image="user.avatar" :size="size"/>
    <v-icon v-else :size="size" class="opacity-70">mdi-account-circle</v-icon>
</template>

<style scoped>

</style>
