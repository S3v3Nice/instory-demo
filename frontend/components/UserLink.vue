<script setup lang="ts">
import type {User} from '~/types'

defineProps({
    user: {
        type: Object as PropType<User | null>,
        required: true
    }
})
</script>

<template>
    <NuxtLink :to="{name: 'users-username', params: {username: user!.username}}">
        <slot/>
    </NuxtLink>
</template>

<style scoped>

</style>
