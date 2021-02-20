import Vue from 'vue'
import VueRouter from 'vue-router'

import SignUp from '@/views/auth/SignUp'
import SignIn from '@/views/auth/SignIn'
import Messenger from '@/views/messenger/Messenger'

Vue.use(VueRouter)

const routes = [
    {
        path: '/auth/signup/',
        name: 'SignUp',
        component: SignUp
    },
    {
        path: '/auth/signin/',
        name: 'SignIn',
        component: SignIn
    },
    {
        path: '/',
        name: 'Messenger',
        component: Messenger
    }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
