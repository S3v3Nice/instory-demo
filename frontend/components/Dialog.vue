<script setup lang="ts">
defineProps({
    title: String,
    backBtn: {
        type: Boolean,
        default: false,
    },
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
const emit = defineEmits(['back', 'close'])
const isOpen = defineModel<boolean>({required: true})

watch(isOpen, (isOpen) => {
    if (!isOpen) {
        emit('close')
    }
})
</script>

<template>
    <v-dialog v-model="isOpen" :max-width="maxWidth" :width="fullWidth ? '100%' : undefined">
        <template v-slot:default="{ isActive }">
            <v-card :rounded="rounded">
                <v-card-title
                    v-if="backBtn || title || closeBtn"
                    class="relative h-[3rem]"
                >
                    <v-btn
                        v-if="backBtn"
                        icon
                        flat
                        class="cursor-pointer absolute left-0 top-1/2 -translate-y-1/2"
                        @click="emit('back')"
                    >
                        <v-icon>mdi-arrow-left</v-icon>
                    </v-btn>

                    <p
                        v-if="title"
                        class="text-base font-semibold absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2"
                    >
                        {{ title }}
                    </p>

                    <v-btn
                        v-if="closeBtn"
                        icon
                        flat
                        class="cursor-pointer absolute right-0 top-1/2 -translate-y-1/2"
                        @click="isActive.value = false"
                    >
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
