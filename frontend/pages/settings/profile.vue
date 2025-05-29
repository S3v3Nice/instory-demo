<script setup lang="ts">
import UsernameChangeForm from '~/components/partials/settings/UsernameChangeForm.vue'

useHead({
    title: 'Profile Settings',
})

definePageMeta({
    requiresAuth: true
})

const authStore = useAuthStore()
const toastStore = useToastStore()
const data = reactive({
    first_name: authStore.firstName!,
    last_name: authStore.lastName!,
})
const errors = ref<{ [key: string]: string[] }>({})
const isSubmitting = ref(false)
const isUsernameChangeDialog = ref(false)

async function submit() {
    isSubmitting.value = true

    try {
        await $api('/settings/profile/', {
            method: 'PUT',
            body: data,
            watch: false
        })

        authStore.user!.first_name = data.first_name
        authStore.user!.last_name = data.last_name
        toastStore.success('Profile updated successfully!')
    } catch (error: any) {
        if (error?.data) {
            errors.value = error.data
            if (error.data.__all__) {
                toastStore.error(error.data.__all__)
            }
        } else {
            toastStore.error('Unknown error occurred')
        }
    } finally {
        isSubmitting.value = false
    }
}

function openAvatarUploadDialog() {
    const input = document.createElement('input')
    input.type = 'file'
    input.accept = '.png, .jpg, .jpeg'
    input.onchange = () => {
        uploadAvatar(input.files![0])
    }
    input.click()
}

async function uploadAvatar(input: File) {
    const formData = new FormData()
    formData.append('avatar', input)

    try {
        const response = await $api<{ avatar: string }>('/settings/profile/avatar/', {
            method: 'PUT',
            body: formData,
        })

        authStore.user!.avatar = response.avatar
        toastStore.success('Avatar updated successfully!')
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
    }
}
</script>

<template>
    <div>
        <h2 class="max-sm:hidden text-xl font-semibold mb-4">Profile Settings</h2>

        <div class="rounded-2xl p-4 mb-6 bg-[var(--surface-light-color)] flex items-center gap-3">
            <Avatar :user="authStore.user!" class="cursor-pointer" title="Upload photo"
                    @click="openAvatarUploadDialog()"/>
            <div class="flex items-center">
                <p class="font-semibold">{{ authStore.username }}</p>
                <v-btn icon="mdi-pencil" variant="text" class="cursor-pointer opacity-50" size="x-small"
                       @click="isUsernameChangeDialog = true"/>
            </div>

            <v-btn
                color="primary"
                variant="flat"
                class="ml-auto normal-case cursor-pointer"
                @click="openAvatarUploadDialog()"
            >
                New photo
            </v-btn>
        </div>

        <v-form @submit.prevent="submit" class="flex flex-col">
            <p class="font-semibold mb-2">First Name</p>
            <v-text-field
                v-model="data.first_name"
                placeholder="First Name"
                variant="outlined"
                :error-messages="errors['first_name']"
                class="mb-2"
            />

            <p class="font-semibold mb-2">Last Name</p>
            <v-text-field
                v-model="data.last_name"
                placeholder="Last Name"
                variant="outlined"
                :error-messages="errors['last_name']"
                class="mb-2"
            />

            <v-btn
                color="primary"
                variant="flat"
                type="submit"
                :disabled="data.first_name === authStore.firstName && data.last_name === authStore.lastName"
                class="ml-auto sm:w-[17rem] w-full cursor-pointer"
            >
                Submit
            </v-btn>
        </v-form>

        <Dialog v-model="isUsernameChangeDialog">
            <UsernameChangeForm @submit="isUsernameChangeDialog = false"/>
        </Dialog>
    </div>
</template>

<style scoped>

</style>
