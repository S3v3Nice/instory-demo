<script setup lang="ts">
const route = useRoute()

const uidb64 = route.params.uidb64
const token = route.params.token
const isLoading = ref(true)
const isError = ref(false)

onMounted(() => {
    $api(`/email/verify/${uidb64}/${token}`, {
        method: 'POST',
    }).catch((err) => {
        isError.value = true
    }).finally(() => {
        isLoading.value = false
    })
})
</script>

<template>
    <div class="flex justify-center h-[80vh] items-center">
        <div v-if="isLoading">
            <v-progress-circular indeterminate size="large"></v-progress-circular>
        </div>
        <div v-else>
            <div v-if="isError" class="flex flex-col gap-2">
                <v-icon icon="mdi-alert-circle" size="64" color="error" class="self-center"/>
                <p class="text-2xl font-semibold text-center">Invalid token</p>
                <p class="opacity-80 text-center">Sorry, it looks like your email verification token is invalid.</p>
            </div>
            <div v-else class="flex flex-col gap-2">
                <v-icon icon="mdi-check-circle" size="64" color="success" class="self-center"/>
                <p class="text-2xl font-semibold text-center">Thank you!</p>
                <p class="opacity-80 text-center">Your email has been successfully verified!</p>
            </div>
            <NuxtLink :to="{name: 'index'}">
                <v-btn
                    color="primary"
                    variant="tonal"
                    prepend-icon="mdi-home"
                    class="flex text-none cursor-pointer max-xl:px-0 min-w-0 w-full mt-6"
                >
                    Go Home
                </v-btn>
            </NuxtLink>
        </div>
    </div>
</template>

<style scoped>

</style>
