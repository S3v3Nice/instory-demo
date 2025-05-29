<script setup lang="ts">
import type {Post, User} from '~/types'

const route = useRoute()
const username = route.params.username as string

useHead({
    title: `@${username}`,
})

const authStore = useAuthStore()

const {
    data: user,
    status: userStatus,
    error: userError,
} = useAsyncData<User | null>(`user-${username}`, () =>
    $api(`/users/${username}/`)
)

const isUserLoading = computed(() => userStatus.value === 'pending')

const {
    data: posts,
    status: postsStatus,
    error: postsError,
    execute: fetchPosts
} = useAsyncData<Post[]>(
    `user-${username}-posts`,
    () => $api(`/users/${username}/posts/`),
    {
        immediate: !!user.value,
    }
)

watch(user, (newUser) => {
    if (newUser && !posts.value) fetchPosts()
})

const isPostsLoading = computed(() => postsStatus.value === 'idle' || postsStatus.value === 'pending')
</script>

<template>
    <div class="flex flex-col items-center">
        <div class="sm:p-0 md:p-6 max-w-4xl w-full flex flex-col gap-2">
            <v-progress-circular
                v-if="isUserLoading"
                indeterminate
                class="self-center justify-self-center min-h-[80vh]"
            />
            <div v-else-if="user" class="flex flex-col">
                <div class="flex flex-col gap-2 border-b">
                    <div class="flex gap-10 max-sm:px-6 max-sm:pt-6">
                        <Avatar :user="user" :size="150" class="max-sm:hidden m-6"/>
                        <Avatar :user="user" :size="77" class="sm:hidden mb-4"/>
                        <div class="sm:mt-6 flex flex-col gap-6">
                            <div class="flex max-sm:flex-col sm:items-center gap-2 sm:gap-4">
                                <p class="text-xl tracking-widest">{{ user.username }}</p>
                                <NuxtLink v-if="user.id === authStore.id" :to="{name: 'settings-profile'}">
                                    <v-btn
                                        color="var(--surface-light-color)"
                                        variant="flat"
                                        class="normal-case font-semibold cursor-pointer"
                                        size="small"
                                    >
                                        Edit profile
                                    </v-btn>
                                </NuxtLink>
                            </div>
                            <div class="flex items-center gap-8 max-sm:hidden">
                                <span class="flex gap-1">
                                    <span class="font-semibold">{{ user.posts_count }}</span>
                                    <span class="opacity-60">posts</span>
                                </span>

                                <span class="flex gap-1">
                                    <span class="font-semibold">{{ user.followers_count }}</span>
                                    <span class="opacity-60">followers</span>
                                </span>

                                <span class="flex gap-1">
                                    <span class="font-semibold">{{ user.following_count }}</span>
                                    <span class="opacity-60">following</span>
                                </span>
                            </div>
                            <p class="max-sm:hidden text-sm font-semibold">
                                {{ user.first_name }} {{ user.last_name }}
                            </p>
                        </div>
                    </div>

                    <p class="sm:hidden mx-7 mb-4 text-sm font-semibold">{{ user.first_name }} {{ user.last_name }}</p>
                </div>

                <div class="sm:hidden flex border-b justify-space-around py-2">
                    <div class="flex flex-col items-center w-1/3">
                        <p class="font-semibold">{{ user.posts_count }}</p>
                        <p class="opacity-60">posts</p>
                    </div>
                    <div class="flex flex-col items-center w-1/3">
                        <p class="font-semibold">{{ user.followers_count }}</p>
                        <p class="opacity-60">followers</p>
                    </div>
                    <div class="flex flex-col items-center w-1/3">
                        <p class="font-semibold">{{ user.following_count }}</p>
                        <p class="opacity-60">following</p>
                    </div>
                </div>

                <div class="flex flex-col">
                    <v-progress-circular
                        v-if="isPostsLoading"
                        indeterminate
                        class="self-center justify-self-center my-10"
                    />
                    <div v-else-if="posts && posts.length" class="grid grid-cols-3 gap-1 mt-4">
                        <NuxtLink
                            v-for="post in posts"
                            :to="{ name: 'posts-id', params: { id: post.id } }"
                            :key="post.id"
                            class="relative w-full overflow-hidden cursor-pointer group"
                            style="aspect-ratio: 3 / 4;"
                        >
                            <!-- Картинка -->
                            <img
                                :src="post.image"
                                alt="Post image"
                                class="absolute inset-0 w-full h-full object-cover"
                            />

                            <div
                                class="absolute inset-0 bg-black/65 opacity-0 group-hover:opacity-100 transition-opacity"></div>

                            <div
                                class="absolute flex inset-0 opacity-0 group-hover:opacity-100 items-center justify-center gap-6 transition-opacity  text-white"
                            >
                                <div class="flex items-center gap-1">
                                    <v-icon size="24" :color="post!.is_liked ? 'red' : undefined">mdi-heart</v-icon>
                                    <span class="font-semibold">{{ post.likes_count }}</span>
                                </div>
                                <div class="flex items-center gap-1">
                                    <v-icon size="24">mdi-comment</v-icon>
                                    <span class="font-semibold">{{ post.comments_count }}</span>
                                </div>
                            </div>
                        </NuxtLink>
                    </div>
                    <div v-else class="text-center opacity-60 mt-4">No posts yet.</div>
                </div>
            </div>
            <div v-else class="flex flex-col items-center justify-center min-h-[80vh] text-center px-4">
                <div class="p-6 max-w-md w-full flex flex-col items-center gap-2">
                    <v-icon size="64" color="error">mdi-magnify-remove-outline</v-icon>
                    <p class="text-2xl font-semibold">User not found</p>
                    <p class="opacity-80">
                        Maybe this user has been deleted or changed their nickname.
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
