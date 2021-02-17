import {baseUrl} from '@/config'

import Vue from 'vue'

export default {
    install () {
        Vue.prototype.$transport = {}

        Vue.prototype.$transport.createUser = async function (/** @type {object} */ user) {
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

            return response.json()
        }
    }
}
