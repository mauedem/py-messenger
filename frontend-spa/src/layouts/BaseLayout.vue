<template>
    <div>
        <navigation @show-confirm-logout-modal="showConfirmLogoutModal"/>

        <v-main>
            <slot></slot>
        </v-main>

        <v-dialog
            v-model="isConfirmLogoutVisible"
            width="400"
        >
            <v-card>
                <v-card-title class="headline text-no-wrap">
                    Подтвердить разлогирование
                </v-card-title>

                <v-card-text class="text-center">
                    Вы уверены, что хотите разлогиниться?
                </v-card-text>

                <v-card-actions class="d-flex">
                    <div class="mx-auto">
                        <v-btn
                            color="secondary lighten-1"
                            text
                            @click="isConfirmLogoutVisible = false"
                        >
                            Отменить
                        </v-btn>

                        <v-btn
                            color="primary"
                            text
                            @click="logoutUser"
                        >
                            Подтвердить
                        </v-btn>
                    </div>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
import Navigation from '@/components/Navigation'

export default {
    name: 'BaseLayout',

    components: {
        Navigation
    },

    data: () => ({
        isConfirmLogoutVisible: false
    }),

    methods: {
        showConfirmLogoutModal () {
            this.isConfirmLogoutVisible = true
        },

        async logoutUser () {
            await this.$transport.logoutUser()

            await this.redirectToSignInPage()
        },

        redirectToSignInPage () {
            this.$router.push({ name: 'SignIn' })
        }
    }
}
</script>
