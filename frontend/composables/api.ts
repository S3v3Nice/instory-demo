export const useApi = (url: string, options: any = {}) => {
    const csrfToken = useCookie('csrftoken')
    const csrfMethods = ['POST', 'PUT', 'PATCH', 'DELETE']
    const method = options.method ? options.method.toUpperCase() : 'GET'

    const requestHeaders = useRequestHeaders(['cookie'])

    return useFetch(url, {
        baseURL: import.meta.client ? '/api/v1' : 'http://backend:8000/api/v1',
        credentials: 'include',
        headers: {
            ...requestHeaders,
            ...options.headers,
            ...(csrfToken.value && csrfMethods.includes(method)
                ? {'X-CSRFToken': csrfToken.value}
                : {}),
        },
        ...options,
    })
}

export const $api = $fetch.create({
    baseURL: import.meta.client ? '/api/v1' : `http://backend:8000/api/v1`,
    credentials: 'include',
    responseType: 'json',
    onRequest({options}) {
        const csrfToken = useCookie('csrftoken')
        const csrfMethods = ['POST', 'PUT', 'PATCH', 'DELETE']
        const method = options.method ? options.method.toUpperCase() : 'GET'

        const headers = useRequestHeaders(['cookie'])

        options.headers = new Headers({
            ...headers,
            ...options.headers,
        })

        if (csrfToken.value && csrfMethods.includes(method)) {
            options.headers.set('X-CSRFToken', csrfToken.value)
        }
    },
})
