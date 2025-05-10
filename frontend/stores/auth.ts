import type {User} from '~/types'
import {defineStore} from 'pinia'

interface AuthUser {
    isAuthenticated: boolean
    isFetched: boolean
    user: User | null
}

export const useAuthStore = defineStore('auth', {
    state: (): AuthUser => ({
        isAuthenticated: false,
        isFetched: false,
        user: null,
    }),
    getters: {
        id: (state: AuthUser) => state.user?.id,
        username: (state: AuthUser) => state.user?.username,
        email: (state: AuthUser) => state.user?.email,
        dateVerifiedEmail: (state: AuthUser) => state.user?.date_verified_email,
        avatar: (state: AuthUser) => state.user?.avatar,
        firstName: (state: AuthUser) => state.user?.first_name,
        lastName: (state: AuthUser) => state.user?.last_name,
        dateJoined: (state: AuthUser) => state.user?.date_joined,
        followers: (state: AuthUser) => state.user?.followers,
        following: (state: AuthUser) => state.user?.following,
        isEmailVerified: (state: AuthUser) => state.user?.date_verified_email !== null,
    },
    actions: {
        async fetchInitialUser() {
            const response = await useApi('/users/me/')
            this.user = response.data.value as User | null
            if (this.user) {
                this.isAuthenticated = true
                this.isFetched = true
            }
        },

        async fetchUser() {
            this.user = await $api<User>('/users/me/')
            if (this.user) {
                this.isAuthenticated = true
                this.isFetched = true
            }
        },

        async reset() {
            this.user = null
            this.isAuthenticated = false
        },
    },
})
