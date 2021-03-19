<template>
    <v-app>
        <auth-page-layout v-if="isAuthPage">
            <router-view/>
        </auth-page-layout>

        <base-layout v-else>
            <keep-alive>
                <router-view/>
            </keep-alive>
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
            return this.$route.path.includes('/auth/')
        }
    }
}
</script>

<style lang="stylus">
@import "styles/main.styl"
</style>
