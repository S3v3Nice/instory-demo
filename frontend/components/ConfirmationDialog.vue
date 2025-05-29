<script setup lang="ts">
defineProps({
    title: {
        type: String,
        required: true,
    },
    description: {
        type: String,
        required: true,
    },
    cancelBtn: {
        type: String,
        default: 'Cancel',
    },
    confirmBtn: {
        type: String,
        default: 'Confirm',
    }
})
const emit = defineEmits(['cancel', 'confirm'])
const isOpen = defineModel<boolean>({required: true})

function onCancel() {
    emit('cancel')
    isOpen.value = false
}

function onConfirm() {
    emit('confirm')
    isOpen.value = false
}
</script>

<template>
    <Dialog v-model="isOpen" :close-btn="false" :full-mobile-width="false" max-width="500" rounded="lg">
        <slot name="title">
            <p class="text-center text-lg mt-5">{{ title }}</p>
        </slot>
        <slot name="description">
            <p class="text-center opacity-70 mx-2">{{ description }}</p>
        </slot>
        <div class="flex flex-col mt-6">
            <v-btn color="primary" variant="text" height="3rem" class="border-t cursor-pointer normal-case"
                   @click="onConfirm">
                {{ confirmBtn }}
            </v-btn>
            <v-btn variant="text" height="3rem" class="border-t cursor-pointer normal-case" @click="onCancel">
                {{ cancelBtn }}
            </v-btn>
        </div>
    </Dialog>
</template>

<style scoped>

</style>
