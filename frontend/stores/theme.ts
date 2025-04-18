import {defineStore} from 'pinia'

const darkThemeCookieName = 'dark-theme'

export const useThemeStore = defineStore('theme', {
    state: () => ({
        isDark: false,
    }),
    getters: {
        isLight: (state) => !state.isDark,
    },
    actions: {
        setTheme(isDark: boolean) {
            this.isDark = isDark

            const darkThemeCookie = useCookie(darkThemeCookieName)
            darkThemeCookie.value = String(isDark)
        },

        toggleTheme() {
            this.setTheme(!this.isDark)
        },

        initFromCookie() {
            const darkThemeCookie = useCookie(darkThemeCookieName)
            this.isDark = !!darkThemeCookie.value
        }
    }
})
