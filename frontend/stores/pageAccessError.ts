import {defineStore} from 'pinia'

export const usePageAccessErrorStore = defineStore('page-access-error', {
    state: () => ({
        authRequired: false,
    }),
})
