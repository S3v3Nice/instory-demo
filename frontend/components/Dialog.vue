<script setup lang="ts">
defineProps({
    closeBtn: {
        type: Boolean,
        default: true,
    },
    rounded: {
        type: [String, Number, Boolean],
        default: 'xl',
    },
    maxWidth: {
        type: [String, Number],
        default: '600',
    },
    fullWidth: {
        type: Boolean,
        default: true,
    }
})
const isOpen = defineModel<boolean>({required: true})
</script>

<template>
    <v-dialog v-model="isOpen" :max-width="maxWidth" :width="fullWidth ? '100%' : undefined">
        <template v-slot:default="{ isActive }">
            <v-card :rounded="rounded">
                <v-card-title v-if="closeBtn" class="w-full flex items-center pb-0">
                    <v-btn icon flat class="cursor-pointer ml-auto -mr-3" @click="isActive.value = false">
                        <v-icon>mdi-close</v-icon>
                    </v-btn>
                </v-card-title>

                <slot/>
            </v-card>
        </template>
    </v-dialog>
</template>

<style scoped>

</style>
