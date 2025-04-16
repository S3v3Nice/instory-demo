import '@mdi/font/css/materialdesignicons.css'

import 'vuetify/styles'
import {createVuetify} from 'vuetify'
import {colors} from 'consola/utils'

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
                        primary: '#FF738C'
                    }
                }
            }
        }
    })
    app.vueApp.use(vuetify)
})
