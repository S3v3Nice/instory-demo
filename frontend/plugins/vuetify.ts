import '@mdi/font/css/materialdesignicons.css'

import 'vuetify/styles'
import {createVuetify} from 'vuetify'
import {useThemeStore} from '~/stores/theme'

export default defineNuxtPlugin((app) => {
    const vuetify = createVuetify({
        theme: {
            themes: {
                light: {
                    colors: {
                        primary: '#FF538C'
                    }
                },
                dark: {
                    colors: {
                        primary: '#D6537A'
                    }
                }
            }
        }
    })

    const themeStore = useThemeStore()
    themeStore.initFromCookie()

    vuetify.theme.global.name.value = themeStore.isDark ? 'dark' : 'light'

    themeStore.$subscribe((mutation, state) => {
        vuetify.theme.global.name.value = state.isDark ? 'dark' : 'light'
    })

    app.vueApp.use(vuetify)
})
