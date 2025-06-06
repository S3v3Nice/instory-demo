import {defineStore} from 'pinia'

export const useModalStore = defineStore('modal', {
    state: () => ({
        authModal: false,
        logoutModal: false,
        postCreateModal: false,
    }),
})
