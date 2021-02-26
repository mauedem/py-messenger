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
                            Регистрация в PyMessenger
                        </v-toolbar-title>
                    </v-toolbar>

                    <v-card-text>
                        <v-form
                            ref="form"
                            v-model="isFormValid"
                            lazy-validation
                        >
                            <v-text-field
                                v-model="form.username"
                                :state="validateState('username')"
                                :error-messages="usernameErrors"
                                label="Логин"
                                required
                                prepend-icon="mdi-account"
                            />

                            <v-text-field
                                v-model="form.nickname"
                                :state="validateState('nickname')"
                                :error-messages="nicknameErrors"
                                label="Имя пользователя"
                                required
                                prepend-icon="mdi-account-outline"
                            />

                            <v-text-field
                                v-model="form.password"
                                :state="validateState('password')"
                                :error-messages="passwordErrors"
                                label="Пароль"
                                prepend-icon="mdi-lock"
                                autocomplete="on"
                                required
                                :append-icon="isPasswordVisibe ? 'mdi-eye' : 'mdi-eye-off'"
                                @click:append="togglePasswordVisibility"
                                :type="isPasswordVisibe ? 'text' : 'password'"
                            >
                            </v-text-field>

                            <v-text-field
                                v-model="form.confirmPassword"
                                :state="validateState('confirmPassword')"
                                :error-messages="confirmPasswordErrors"
                                label="Подтвердить пароль"
                                prepend-icon="mdi-lock-outline"
                                autocomplete="on"
                                required
                                :type="isPasswordVisibe ? 'text' : 'password'"
                            >
                            </v-text-field>
                        </v-form>
                    </v-card-text>

                    <v-card-actions class="d-flex">
                        <v-btn class="px-16 mx-auto mb-3"
                               color="primary"
                               @click="registerUser"
                        >
                            Зарегистрироваться
                        </v-btn>
                    </v-card-actions>
                </v-card>

                <div class="d-flex">
                    <v-btn to="/auth/signin/"
                           text
                           class="mx-auto mt-3"
                    >
            <span class="redirect-button">
                Уже есть аккаунт
            </span>
                    </v-btn>
                </div>
            </v-col>
        </v-row>

        <v-snackbar
            v-model="isUserExistsError"
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

            Пользователь с таким именем уже существует
        </v-snackbar>

        <v-snackbar
            v-model="isUserRegisteredSuccessfully"
            :timeout="2000"
            absolute
            bottom
            shaped
            color="success"
            @input="v => v || redirectToSignInPage()"
        >
            <template>
                <v-btn text
                       class="d-inline-block">
                    <v-icon>mdi-checkbox-marked-circle</v-icon>
                </v-btn>
            </template>

            <span class="body-2 font-weight-bold">Пользователь успешно зарегистрирован</span>
            <p class="center">Сейчас вы будете перенаправлены на страницу входа</p>
        </v-snackbar>
    </v-container>
</template>

<script>
import { myValidationMixin } from '@/mixins/validationMixin'
import { required, minLength, maxLength, sameAs } from 'vuelidate/lib/validators'

export default {
    name: 'SignUp',

    mixins: [myValidationMixin],

    data: () => ({
        form: {
            username: '',
            nickname: '',
            password: '',
            confirmPassword: ''
        },

        isFormValid: true,

        isPasswordVisibe: false,

        isUserExistsError: false,
        isUserRegisteredSuccessfully: false
    }),

    validations: {
        form: {
            username: {
                required,
                minLength: minLength(4),
                maxLength: maxLength(120)
            },

            nickname: { required },

            password: { required },
            confirmPassword: {
                required,
                sameAs: sameAs('password')
            }
        }
    },

    computed: {
        usernameErrors () {
            const errors = []

            if (!this.$v.form.username.$dirty) return errors
            !this.$v.form.username.required &&
                errors.push('Это поле обязательно для заполнения')
            !this.$v.form.username.minLength &&
                errors.push('Минимальная длина этого поля 4 символа')
            !this.$v.form.username.maxLength &&
                errors.push('Максимальная длина этого поля 120 символов')

            return errors
        },

        nicknameErrors () {
            const errors = []

            if (!this.$v.form.nickname.$dirty) return errors
            !this.$v.form.nickname.required &&
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

        confirmPasswordErrors () {
            const errors = []

            if (!this.$v.form.confirmPassword.$dirty) return errors
            !this.$v.form.confirmPassword.required &&
                errors.push('Это поле обязательно для заполнения')
            !this.$v.form.confirmPassword.sameAs &&
                errors.push("Поле должно совпадать с полем 'Пароль'")

            return errors
        }
    },

    methods: {
        togglePasswordVisibility () {
            this.isPasswordVisibe = !this.isPasswordVisibe
        },

        async registerUser () {
            if (!this.checkFormValidation()) return

            try {
                await this.$transport.registerUser({
                    username: this.form.username,
                    nickname: this.form.nickname,
                    password: this.form.password
                })

                this.isUserRegisteredSuccessfully = true
            } catch (err) {
                this.isUserExistsError = true
            }
        },

        redirectToSignInPage () {
            this.$router.push({ name: 'SignIn' })
        }
    }
}
</script>
