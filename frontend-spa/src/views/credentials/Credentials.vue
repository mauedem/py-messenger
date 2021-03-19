<template>
    <v-container
        style="height: 100vh"
        fluid
    >
        <v-card
            class="mx-5 my-4"
            :class="!isSuccessfullyTelegramAuthorized ? 'py-4' : 'py-2'"
            outlined
            elevation="2"
        >
            <v-list-item three-line>
                <v-avatar
                    class="mr-3"
                    color="primary"
                    :size="!isSuccessfullyTelegramAuthorized ? 70 : 100"
                >
                    <img
                        v-if="!isSuccessfullyTelegramAuthorized"
                        src="http://localhost/media/avatars/777000.jpg"
                        alt="Avatar"
                    />

                    <img
                        v-else
                        :src="getTelegramUserAvatar"
                        alt="Avatar"
                    />
                </v-avatar>

                <v-list-item-content>
                    <v-list-item-title class="headline mb-1 ml-3">
                        Telegram
                    </v-list-item-title>

                    <v-list-item-subtitle
                        v-if="!isSuccessfullyTelegramAuthorized"
                        class="ml-3"
                    >
                        Войти в свой телеграм аккаунт
                    </v-list-item-subtitle>

                    <div v-else>
                        <v-list-item class="mt-0">
                            <span class="font-weight-bold">{{ getUserName }}</span>
                        </v-list-item>

                        <v-list-item>
                            <span class="text--secondary mt-n12">
                                {{ user.phone | VMask('+#(###)###-##-##') }}
                            </span>
                        </v-list-item>

                        <v-list-item
                            v-if="user.username"
                            class="mt-n12"
                            >
                            <span class="text--secondary">@{{ user.username }}</span>
                        </v-list-item>
                    </div>
                </v-list-item-content>

                <v-card-actions>
                    <auth-telegram-modal
                        v-if="!isSuccessfullyTelegramAuthorized"
                        @authorize-telegram="authorizeTelegram"
                        :is-code-sending="isCodeSending"
                        :is-code-sent="isCodeSent"
                    />

                    <logout-telegram-modal
                        v-else
                        @logout-telegram="logoutTelegram"
                    >

                    </logout-telegram-modal>
                </v-card-actions>
            </v-list-item>

            <v-progress-linear
                :active="!isAuthorizedTelegramLoaded"
                indeterminate
                absolute
                bottom
                color="deep-purple accent-4"
            ></v-progress-linear>
        </v-card>

        <v-snackbar
            v-model="isSuccessfullyNotificationVisible"
            :timeout="4000"
            absolute
            bottom
            shaped
            color="success"
        >
            <template>
                <v-btn text
                       class="d-inline-block">
                    <v-icon>mdi-checkbox-marked-circle</v-icon>
                </v-btn>
            </template>

            <span class="center">
                {{ getNotificationMessage }}
            </span>
        </v-snackbar>
    </v-container>
</template>

<script>
import AuthTelegramModal from '@/components/credentials/AuthTelegramModal'
import LogoutTelegramModal from '@/components/credentials/LogoutTelegramModal'
import { VueMaskFilter } from 'v-mask'

export default {
    name: 'Credentials',

    components: {
        AuthTelegramModal,
        LogoutTelegramModal
    },

    data: () => ({
        isAuthorizedTelegramLoaded: true,

        isCodeSending: false,
        isCodeSent: false,

        isSuccessfullyNotificationVisible: false,
        isSuccessfullyTelegramAuthorized: false,

        user: {}
    }),

    computed: {
        getUserName () {
            if (this.user.first_name && this.user.last_name) {
                return `${this.user.first_name} ${this.user.last_name}`
            } else if (this.user.first_name || this.user.last_name) {
                return this.user.first_name || this.user.last_name
            }

            return this.user.username
        },

        getTelegramUserAvatar () {
            if (this.isSuccessfullyTelegramAuthorized) {
                return 'http://localhost/media/avatars/user_avatar.jpg'
            }

            return ''
        },

        getNotificationMessage () {
            if (this.isSuccessfullyTelegramAuthorized) {
                return `Вы успешно вошли в Telegram как ${this.getUserName}`
            }

            return 'Успешный выход из Telegram'
        }
    },

    filters: {
        VMask: VueMaskFilter
    },

    methods: {
        async authorizeTelegram (/** @type {object} */ user) {
            let userCredentials = this.user

            if (!user.code) {
                userCredentials = {
                    phone_number: user.phoneNumber
                }

                if (user.password) {
                    userCredentials.password = user.password
                }

                this.user = userCredentials
            } else {
                this.user.code = user.code
            }

            try {
                user.code ? this.isAuthorizedTelegramLoaded = false
                    : this.isCodeSending = true

                this.user = await this.$transport.authorizeTelegramUser(this.user)

                this.isAuthorizedTelegramLoaded = true
                this.isSuccessfullyNotificationVisible = true
                this.isSuccessfullyTelegramAuthorized = true
            } catch (err) {
                this.isCodeSending = false

                const { message } = err

                if (message === '449') {
                    this.isCodeSent = true
                }
            }
        },

        async logoutTelegram () {
            try {
                await this.$transport.logoutTelegramUser()

                this.user = {}
                this.isSuccessfullyTelegramAuthorized = false
                this.isSuccessfullyNotificationVisible = true
            } catch (err) {
                const { message } = err

                console.log(message)
            }
        }
    },

    created () {
        if (Object.keys(this.$store.state.currentUser.telegram_credentials).length !== 0) {
            this.user = this.$store.state.currentUser.telegram_credentials
            this.isSuccessfullyTelegramAuthorized = true
        }
    }
}
</script>
