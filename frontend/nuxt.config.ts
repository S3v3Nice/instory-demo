import vuetify, {transformAssetUrls} from 'vite-plugin-vuetify'
import {defineNuxtModule} from '@nuxt/kit'
import tailwindcss from '@tailwindcss/vite'

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    compatibilityDate: '2024-11-01',
    devtools: {enabled: true},
    build: {
        transpile: ['vuetify'],
    },
    modules: [
        defineNuxtModule({
            setup(_options, nuxt) {
                nuxt.hooks.hook('vite:extendConfig', (config) => {
                    // @ts-expect-error
                    config.plugins.push(vuetify({autoImport: true, styles: {configFile: 'assets/css/vuetify.scss'}}))
                })
            }
        }),
        '@pinia/nuxt'
    ],
    css: [
        '~/assets/css/main.scss',
        '~/assets/css/tailwind.css'
    ],
    pinia: {
        autoImports: ['defineStore'],
        disableVuex: true
    },
    vite: {
        vue: {
            template: {
                // Need this to resolve relative asset URLs that are passed to
                // Vuetify components such as VImg (e.g. ~/assets/img/some.png).
                transformAssetUrls,
            },
        },
        plugins: [
            tailwindcss(),
        ],
    },
})
