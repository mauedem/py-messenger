import { baseUrl, staticUrl } from '@/config'

import Vue from 'vue'

export default {
    install () {
        Vue.prototype.$transport = {}

        Vue.prototype.$transport.registerUser = async function (/** @type {object} */ user) {
            const url = `${baseUrl}/auth/register/`

            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json;charset=utf-8'
                },
                body: JSON.stringify(user)
            })

            if (!response.ok) {
                throw new Error(`Bad response: ${response.status}`)
            }

            return response
        }

        Vue.prototype.$transport.authorizeUser = async function (/** @type {object} */ user) {
            const url = `${baseUrl}/auth/login/`

            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json;charset=utf-8'
                },
                body: JSON.stringify(user)
            })

            if (!response.ok) {
                throw new Error(`Bad response: ${response.status}`)
            }
        }

        Vue.prototype.$transport.getAuthorizedUser = async function () {
            const url = `${baseUrl}/auth/authenticate/`

            const response = await fetch(url)

            if (!response.ok) {
                throw new Error(`Bad response: ${response.status}`)
            }

            return response.json()
        }

        Vue.prototype.$transport.logoutUser = async function () {
            const url = `${baseUrl}/auth/logout/`

            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json;charset=utf-8'
                }
            })

            if (!response.ok) {
                throw new Error(`Bad response: ${response.status}`)
            }
        }

        Vue.prototype.$transport.authorizeTelegramUser = async function (/** @type {object} */ user) {
            const url = `${baseUrl}/tg/authorize/`

            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json;charset=utf-8'
                },
                body: JSON.stringify(user)
            })

            if (!response.ok) {
                console.log(response.status)
                throw new Error(`${response.status}`)
            }

            return response.json()
        }

        Vue.prototype.$transport.logoutTelegramUser = async function () {
            const url = `${baseUrl}/tg/logout/`

            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json;charset=utf-8'
                }
            })

            if (!response.ok) {
                console.log(response.status)
                throw new Error(`${response.status}`)
            }

            return response.json()
        }

        Vue.prototype.$transport.getTelegramDialogs = async function () {
            const url = `${baseUrl}/tg/dialogs/`

            const response = await fetch(url)

            if (!response.ok) {
                console.log(response.status)
                throw new Error(`${response.status}`)
            }

            return response.json()
        }
    }
}
