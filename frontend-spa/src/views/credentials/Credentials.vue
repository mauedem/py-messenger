<template>
    <v-container
        style="height: 100vh"
        fluid
    >
        <v-card
            class="mx-5 my-4"
            :class="!isSuccessfullyTelegramAuthorized ? 'py-4' : 'py-2'"
            outlined
            elevation="1"
        >
            <v-list-item three-line>
                <v-avatar
                    class="mr-3"
                    color="primary"
                    :size="!isSuccessfullyTelegramAuthorized ? 70 : 120"
                >
                    <img
                        v-if="!isSuccessfullyTelegramAuthorized"
                        src="http://localhost/media/messengers/telegram.jpg"
                        alt="Telegram"
                    />

                    <v-img
                        v-else-if="isSuccessfullyTelegramAuthorized && hasUserTelegramAvatar"
                        src="http://localhost/media/avatars/user_avatar.jpg"
                        @error="errorHasHappened"
                    />

                    <span
                        v-else-if="isSuccessfullyTelegramAuthorized && !hasUserTelegramAvatar"
                        class="white--text headline mx-auto"
                    >
                        {{ currentUser.username[0].toUpperCase() }}
                    </span>
                </v-avatar>

                <v-list-item-content>
                    <v-list-item-title class="headline mb-1 ml-3">
                        Telegram

                        <svg-icon
                            v-if="isSuccessfullyTelegramAuthorized"
                            class="mb-n1"
                            icon-name="telegram"
                            style="stroke: #212121"
                        />
                    </v-list-item-title>

                    <v-list-item-subtitle
                        v-if="!isSuccessfullyTelegramAuthorized"
                        class="ml-3"
                    >
                        Войти в свой телеграм аккаунт
                    </v-list-item-subtitle>

                    <div v-else>
                        <v-list-item class="mt-0">
                            <span class="font-weight-bold">
                                {{ getTelegramUserName }}
                            </span>
                        </v-list-item>

                        <v-list-item>
                            <span class="text--secondary mt-n12">
                                {{ telegramUser.phone | VMask('+#(###)###-##-##') }}
                            </span>
                        </v-list-item>

                        <v-list-item
                            v-if="telegramUser.username"
                            class="mt-n12"
                            >
                            <span class="text--secondary">@{{ telegramUser.username }}</span>
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
            v-model="isUnsuccessfulNotificationVisible"
            :timeout="5000"
            color="error"
            shaped
            absolute
            bottom
        >

            <template>
                <v-btn text>
                    <v-icon>mdi-alert</v-icon>
                </v-btn>
            </template>

            Неверные учетные данные
        </v-snackbar>

        <v-snackbar
            v-model="isSuccessfulNotificationVisible"
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
import SvgIcon from '@/components/common/SvgIcon'
import AuthTelegramModal from '@/components/credentials/AuthTelegramModal'
import LogoutTelegramModal from '@/components/credentials/LogoutTelegramModal'
import { VueMaskFilter } from 'v-mask'

export default {
    name: 'Credentials',

    components: {
        SvgIcon,
        AuthTelegramModal,
        LogoutTelegramModal
    },

    data: () => ({
        isAuthorizedTelegramLoaded: true,
        isCodeSending: false,
        isCodeSent: false,

        isSuccessfulNotificationVisible: false,
        isSuccessfullyTelegramAuthorized: false,
        isUnsuccessfulNotificationVisible: false,

        hasUserTelegramAvatar: true,

        currentUser: {},
        telegramUser: {}
    }),

    computed: {
        getTelegramUserName () {
            if (this.telegramUser.first_name && this.telegramUser.last_name) {
                return `${this.telegramUser.first_name} ${this.telegramUser.last_name}`
            } else if (this.telegramUser.first_name ||
                this.telegramUser.last_name) {
                return this.telegramUser.first_name ||
                    this.telegramUser.last_name
            }

            return this.telegramUser.nickname
        },

        getNotificationMessage () {
            if (this.isSuccessfullyTelegramAuthorized) {
                return `Вы успешно вошли в Telegram как ${this.getTelegramUserName}`
            }

            return 'Успешный выход из Telegram'
        }
    },

    filters: {
        VMask: VueMaskFilter
    },

    methods: {
        async authorizeTelegram (/** @type {object} */ user) {
            let userCredentials = this.telegramUser

            if (!user.code) {
                userCredentials = {
                    phone_number: user.phoneNumber
                }

                if (user.password) {
                    userCredentials.password = user.password
                }

                this.telegramUser = userCredentials
            } else {
                this.telegramUser.code = user.code
            }

            try {
                user.code ? this.isAuthorizedTelegramLoaded = false
                    : this.isCodeSending = true

                this.telegramUser = await this.$transport.authorizeTelegramUser(this.telegramUser)

                const authorizedUser = await this.$transport.getAuthorizedUser()
                this.$store.commit('SET_CURRENT_USER', authorizedUser)

                this.isSuccessfulNotificationVisible = true
                this.isSuccessfullyTelegramAuthorized = true
            } catch (err) {
                this.isCodeSending = false

                if (user.code) {
                    this.isUnsuccessfulNotificationVisible = true
                }

                const { message } = err

                if (message === '449') {
                    this.isCodeSent = true
                }
            } finally {
                this.isAuthorizedTelegramLoaded = true
            }
        },

        async logoutTelegram () {
            try {
                await this.$transport.logoutTelegramUser()

                this.currentUser.telegram_credentials = null

                this.$store.commit('SET_CURRENT_USER', this.currentUser)

                this.telegramUser = {}
                this.isSuccessfullyTelegramAuthorized = false
                this.isSuccessfulNotificationVisible = true
            } catch (err) {
                const { message } = err

                console.log(message)
            }
        },

        errorHasHappened () {
            console.log('No avatar. Why?')
            this.hasUserTelegramAvatar = false
        }
    },

    created () {
        this.currentUser = this.$store.state.currentUser

        this.telegramUser = this.$store.state.currentUser.telegram_credentials

        this.isSuccessfullyTelegramAuthorized = !!this.$store.state.currentUser.telegram_credentials
    }
}
</script>
