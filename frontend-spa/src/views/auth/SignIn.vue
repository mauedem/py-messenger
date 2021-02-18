<template>
    <v-container
        class="fill-height"
        fluid
    >
        <v-row
            align="center"
            justify="center"
        >
            <v-col
                cols="12"
                sm="8"
                md="6"
                lg="5"
            >
                <v-card
                    class="elevation-12"
                >
                    <v-toolbar
                        color="primary"
                        dark
                        flat
                    >
                        <v-toolbar-title class="text-center">
                            Авторизуйтесь в PyMessenger
                        </v-toolbar-title>
                    </v-toolbar>

                    <v-card-text>
                        <v-form>
                            <v-text-field
                                v-model="form.login"
                                :state="validateState('login')"
                                :error-messages="loginErrors"
                                label="Логин"
                                prepend-icon="mdi-account"
                            />

                            <v-text-field
                                v-model="form.password"
                                :state="validateState('password')"
                                :error-messages="passwordErrors"
                                label="Пароль"
                                prepend-icon="mdi-lock"
                                autocomplete="on"
                                :append-icon="isPasswordVisibe ? 'mdi-eye' : 'mdi-eye-off'"
                                @click:append="togglePasswordVisibility"
                                :type="isPasswordVisibe ? 'text' : 'password'"
                            >
                            </v-text-field>
                        </v-form>
                    </v-card-text>

                    <v-card-actions class="d-flex">
                        <v-btn class="px-16 mx-auto mb-3"
                               color="primary"
                               @click="authorizeUser"
                        >
                            Войти
                        </v-btn>
                    </v-card-actions>
                </v-card>

                <div class="d-flex">
                    <v-btn to="/auth/signup/"
                           text
                           class="mx-auto mt-3"
                    >
                        <span class="redirect-button">
                            Создать аккаунт
                        </span>
                    </v-btn>
                </div>
            </v-col>
        </v-row>

        <v-snackbar
            v-model="invalidCredentialsError"
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

            Неверный логин или пароль
        </v-snackbar>
    </v-container>
</template>

<script>
import { myValidationMixin } from '@/mixins/validationMixin'
import { required } from 'vuelidate/lib/validators'

export default {
    name: 'SignIn',

    mixins: [myValidationMixin],

    data: () => ({
        form: {
            login: '',
            password: ''
        },

        isPasswordVisibe: false,

        invalidCredentialsError: false
    }),

    validations: {
        form: {
            login: { required },
            password: { required }
        }
    },

    computed: {
        loginErrors () {
            const errors = []

            if (!this.$v.form.login.$dirty) return errors
            !this.$v.form.login.required &&
                errors.push('Это поле обязательно для заполнения')

            return errors
        },

        passwordErrors () {
            const errors = []

            if (!this.$v.form.password.$dirty) return errors
            !this.$v.form.password.required &&
                errors.push('Это поле обязательно для заполнения')

            return errors
        },
    },

    methods: {
        togglePasswordVisibility () {
            this.isPasswordVisibe = !this.isPasswordVisibe
        },

        async authorizeUser () {
            if (!this.checkFormValidation()) return

            try {
                await this.$transport.authorizeUser(this.form)
            } catch (err) {
                this.invalidCredentialsError = true
            }
        }
    }
}
</script>
