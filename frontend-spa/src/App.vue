<template>
    <v-app>
        <auth-page-layout v-if="isAuthPage">
            <router-view />
        </auth-page-layout>

        <base-layout v-else>
            <router-view />
        </base-layout>
    </v-app>
</template>

<script>
import AuthPageLayout from '@/layouts/AuthPageLayout'
import BaseLayout from '@/layouts/BaseLayout'

export default {
    name: 'App',

    components: {
        AuthPageLayout,
        BaseLayout
    },

    computed: {
        isAuthPage () {
            return this.$route.path === '/' ||
                this.$route.path.includes('/auth/')
        }
    }
}
</script>
