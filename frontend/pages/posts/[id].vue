<script setup lang="ts">
import type {Post} from '~/types'
import UserLink from '~/components/UserLink.vue'

useHead({
    title: 'Post',
})

const route = useRoute()
const toastStore = useToastStore()
const id = route.params.id

const {
    data: post,
    status: postStatus,
    error: postError,
} = useAsyncData<Post | null>(`post-${id}`, () =>
    $api(`/posts/${id}/`)
)

const isPostLoading = computed(() => postStatus.value === 'pending')

async function toggleLike() {
    const isLike = !post.value!.is_liked
    post.value!.is_liked = isLike
    post.value!.likes_count += isLike ? 1 : -1

    try {
        await $api(`/posts/${id}/likes/`, {
            method: isLike ? 'POST' : 'DELETE',
        })
    } catch (error: any) {
        toastStore.error('Internal error occurred')
        post.value!.is_liked = !isLike
        post.value!.likes_count += isLike ? -1 : 1
    }
}
</script>

<template>
    <div class="flex justify-center min-h-[100px] items-center">
        <div class="sm:p-4 max-w-5xl w-full flex flex-col gap-2">
            <v-progress-circular
                v-if="isPostLoading"
                indeterminate
                class="self-center justify-self-center min-h-[80vh]"
            />
            <div v-else-if="post" class="flex max-sm:flex-col items-stretch sm:min-h-[450px] justify-center">
                <div class="flex items-center gap-2 p-4 sm:hidden">
                    <UserLink :user="post.user">
                        <Avatar :user="post.user" :size="32"/>
                    </UserLink>
                    <UserLink :user="post.user">
                        <p class="hover:opacity-60 transition">{{ post.user.username }}</p>
                    </UserLink>
                </div>

                <div class="min-w-0 flex justify-center sm:justify-end sm:border">
                    <img
                        :src="post.image"
                        alt="Post image"
                        class="object-contain sm:max-h-[600px]"
                    />
                </div>

                <div class="sm:w-[335px] p-4 shrink-0 flex flex-col gap-2 sm:border-y sm:border-r">
                    <div class="flex items-center gap-2 max-sm:hidden">
                        <UserLink :user="post.user">
                            <Avatar :user="post.user" :size="32"/>
                        </UserLink>
                        <UserLink :user="post.user">
                            <p class="hover:opacity-60 transition">{{ post.user.username }}</p>
                        </UserLink>
                    </div>
                    {{ post.description }}
                    <div class="flex gap-4">
                        <div class="flex -ml-2 items-center">
                            <v-btn
                                :icon="post!.is_liked ? 'mdi-heart' : 'mdi-heart-outline'"
                                variant="text"
                                :color="post!.is_liked ? 'red' : 'grey'"
                                width="40"
                                height="40"
                                class="cursor-pointer"
                                @click="toggleLike"
                            />
                            <p class="text-center font-semibold text-sm">{{ post.likes_count }}</p>
                        </div>
                        <div class="flex items-center">
                            <v-btn
                                icon="mdi-comment-outline"
                                variant="text"
                                color="grey"
                                width="40"
                                height="40"
                                class="cursor-pointer"
                            />
                            <p class="text-center font-semibold text-sm">{{ post.comments_count }}</p>
                        </div>
                    </div>
                </div>
            </div>
            <div v-else class="flex flex-col items-center justify-center min-h-[80vh] text-center px-4">
                <div class="p-6 max-w-md w-full flex flex-col items-center gap-2">
                    <v-icon size="64" color="error">mdi-magnify-remove-outline</v-icon>
                    <p class="text-2xl font-semibold">Post not found</p>
                    <p class="opacity-80">
                        Maybe this post has been deleted or the link is broken.
                    </p>
                    <NuxtLink :to="{name: 'index'}">
                        <v-btn
                            color="primary"
                            variant="tonal"
                            class="mt-4 w-full cursor-pointer"
                        >
                            Home
                        </v-btn>
                    </NuxtLink>
                </div>
            </div>
        </div>
    </div>
</template>


<style scoped>

</style>
