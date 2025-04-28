import {defineStore} from 'pinia'

interface ToastStore {
    successes: string[],
    errors: string[]
}

export const useToastStore = defineStore('toast', {
    state: (): ToastStore => ({
        successes: [],
        errors: []
    }),
    actions: {
        success(message: string) {
            this.successes.push(message)
        },

        error(message: string) {
            this.errors.push(message)
        }
    }
})
