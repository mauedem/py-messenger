import Vue from 'vue'
import VueRouter from 'vue-router'
import SignUp from '@/views/auth/SignUp'
import SignIn from '@/views/auth/SignIn'

Vue.use(VueRouter)

const routes = [
    {
        path: '/auth/signup/',
        name: 'SignUp',
        component: SignUp
    },
    {
        path: '/',
        name: 'SignIn',
        component: SignIn
    }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
