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
        avatar: (state: AuthUser) => state.user?.avatar,
        first_name: (state: AuthUser) => state.user?.first_name,
        last_name: (state: AuthUser) => state.user?.last_name,
        date_joined: (state: AuthUser) => state.user?.date_joined,
        followers: (state: AuthUser) => state.user?.followers,
        following: (state: AuthUser) => state.user?.following,
    },
    actions: {
        async fetchUser() {
            useFetch('/api/v1/auth/')
        }
    }
})
