<script setup lang="ts">
const toastStore = useToastStore()
const isOpen = defineModel<boolean>({required: true})
const isDraggingOver = ref(false)
const imageFile = ref<File>()
const imageFileUrl = computed(() => imageFile.value ? URL.createObjectURL(imageFile.value) : null)
const description = ref('')
const isSubmitting = ref(false)

function onDragEnter() {
    isDraggingOver.value = true
}

function onDragLeave() {
    isDraggingOver.value = false
}

function onDrop(event: DragEvent) {
    if (event.dataTransfer?.files) {
        uploadImage(event.dataTransfer.files[0])
    }
    isDraggingOver.value = false
}

function openImageUploadDialog() {
    const input = document.createElement('input')
    input.type = 'file'
    input.accept = '.png, .jpg, .jpeg'
    input.onchange = () => {
        uploadImage(input.files![0])
    }
    input.click()
}

function uploadImage(file: File) {
    imageFile.value = file
}

async function submit() {
    isSubmitting.value = true

    const formData = new FormData()
    formData.append('image', imageFile.value!)
    formData.append('description', description.value)

    try {
        await $api<{ avatar: string }>('/posts/', {
            method: 'POST',
            body: formData,
        })

        isOpen.value = false
        toastStore.success('Post has been successfully created!')
    } catch (error: any) {
        if (error?.data) {
            if (error.data.avatar) {
                toastStore.error(error.data.avatar[0])
            } else if (error.data.__all__) {
                toastStore.error(error.data.__all__)
            }
        } else {
            toastStore.error('Unknown error occurred')
        }
    } finally {
        isSubmitting.value = false
    }
}

watch(isOpen, (isOpen) => {
    if (isOpen) {
        imageFile.value = undefined
    }
})
</script>

<template>
    <Dialog v-model="isOpen" title="Creating post" :max-width="800">
        <div class="flex w-full justify-center h-[500px] overflow-hidden border-t max-sm:flex-col">
            <!-- Left side / Upper part on mobile -->
            <div class="flex flex-col flex-grow min-w-0 max-sm:max-h-[200px] max-sm:flex-shrink-0">
                <div
                    v-if="imageFileUrl"
                    class="flex-grow flex items-center justify-center overflow-hidden bg-[var(--surface-light-color)]"
                >
                    <img
                        :src="imageFileUrl"
                        alt="Image"
                        class="w-full h-full object-contain sm:border-r"
                    />
                </div>
                <div
                    v-else
                    class="flex flex-col gap-4 flex-grow items-center justify-center transition duration-300"
                    :class="{ 'bg-[var(--surface-light-color)]': isDraggingOver }"
                    @dragenter.prevent="onDragEnter"
                    @dragleave="onDragLeave"
                    @dragover.prevent
                    @drop.prevent="onDrop"
                >
                    <v-icon
                        size="50"
                        :color="isDraggingOver ? 'primary' : undefined"
                        class="transition duration-300"
                    >
                        mdi-image-multiple-outline
                    </v-icon>
                    <p class="text-lg">Drag and drop a picture in here</p>
                    <v-btn
                        color="primary"
                        variant="flat"
                        class="text-none cursor-pointer"
                        @click="openImageUploadDialog"
                    >
                        Select from files
                    </v-btn>
                </div>
            </div>

            <!-- Right side / Bottom part on mobile -->
            <div
                v-if="imageFileUrl"
                class="sm:min-w-[300px] flex flex-col flex-grow max-sm:flex-grow max-sm:overflow-auto"
            >
                <v-textarea v-model="description" placeholder="Description..." variant="plain" no-resize class="px-2"/>
                <v-btn
                    color="primary"
                    variant="flat"
                    class="mb-4 w-full cursor-pointer"
                    :loading="isSubmitting"
                    @click="submit"
                >
                    Create
                </v-btn>
            </div>
        </div>
    </Dialog>


</template>

<style scoped>

</style>
