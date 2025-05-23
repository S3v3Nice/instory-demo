<script setup lang="ts">
import type {Post} from '~/types'
import UserLink from '~/components/UserLink.vue'

useHead({
    title: 'Post',
})

const route = useRoute()
const id = route.params.id

const {
    data: post,
    status: postStatus,
    error: postError,
} = useAsyncData<Post | null>(`post-${id}`, () =>
    $api(`/posts/${id}/`)
)

const isPostLoading = computed(() => postStatus.value === 'pending')
</script>

<template>
    <div class="flex justify-center min-h-[100px] items-center">
        <div class="sm:p-4 max-w-5xl w-full flex flex-col gap-2">
            <div v-if="isPostLoading">Loading...</div>
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
                </div>
            </div>
            <div v-else>
                Post not found!
            </div>
        </div>
    </div>
</template>


<style scoped>

</style>
