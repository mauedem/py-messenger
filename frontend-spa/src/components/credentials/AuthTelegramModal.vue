<template>
    <v-dialog
        v-model="isDialogVisible"
        max-width="600px"
    >
        <template v-slot:activator="{ on, attrs }">
            <v-btn
                color="primary"
                outlined
                v-bind="attrs"
                v-on="on"
            >
                Авторизоваться
            </v-btn>
        </template>

        <v-card>
            <v-card-title>
                <span class="headline">Aвторизация Telegram</span>
            </v-card-title>

            <div v-if="!isCodeSent">
                <v-card-text>
                    <v-form class="pa-3">
                        <v-row>
                            <v-text-field
                                v-model="form.phoneNumber"
                                :state="validateState('phoneNumber')"
                                :error-messages="phoneNumberErrors"
                                label="Номер телефона"
                                v-mask="phoneMask"
                                @keypress="isNumber"
                                return-masked-value
                                prepend-icon="mdi-phone"
                            />
                        </v-row>

                        <v-row align="center">
                            <v-checkbox
                                v-model="is2FA"
                                hide-details
                                class="shrink mr-2 mt-n2"
                            ></v-checkbox>
                            <v-text-field
                                label="Пароль"
                                v-model="form.password"
                                :state="validateState('password')"
                                :error-messages="passwordErrors"
                            />
                        </v-row>
                    </v-form>
                </v-card-text>

                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                        color="secondary lighten-1"
                        text
                        @click="closeDialog"
                    >
                        Отменить
                    </v-btn>
                    <v-btn
                        color="primary"
                        text
                        @click="authorizeTelegram"
                    >
                        Получить код
                    </v-btn>
                </v-card-actions>
            </div>

            <div v-else>
                <v-card-text>
                    <v-text-field
                        v-model="form.code"
                        :state="validateState('code')"
                        :error-messages="codeErrors"
                        label="Код подтверждения"
                        @keypress="isNumber"
                        return-masked-value
                        prepend-icon="mdi-lock-open-check"
                    />
                </v-card-text>

                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                        color="secondary lighten-1"
                        text
                        @click="closeDialog"
                    >
                        Отменить
                    </v-btn>
                    <v-btn
                        color="primary"
                        text
                        @click="authorizeTelegram"
                    >
                        Войти
                    </v-btn>
                </v-card-actions>
            </div>

            <v-progress-linear
                :active="isCodeSending"
                indeterminate
                absolute
                bottom
                color="deep-purple accent-4"
            ></v-progress-linear>
        </v-card>
    </v-dialog>
</template>

<script>
import { myValidationMixin } from '@/mixins/validationMixin'
import {
    maxLength,
    minLength,
    requiredIf
} from 'vuelidate/lib/validators'
import { VueMaskDirective } from 'v-mask'

export default {
    name: 'AuthTelegramModal',

    props: {
        isCodeSending: {
            type: Boolean,
            default: false
        },

        isCodeSent: {
            type: Boolean,
            default: false
        }
    },

    mixins: [myValidationMixin],

    data: () => ({
        isDialogVisible: false,

        is2FA: false,

        form: {
            phoneNumber: '',
            password: '',
            code: ''
        },

        phoneMask: '+7(###)###-##-##'
    }),

    validations: {
        form: {
            phoneNumber: {
                requiredIf: requiredIf(function () {
                    return !this.isCodeSent
                }),
                minLength: minLength(16),
                maxLength: maxLength(16)
            },

            password: {
                requiredIf: requiredIf(function () {
                    return this.is2FA && !this.isCodeSent
                })
            },

            code: {
                requiredIf: requiredIf(function () {
                    return this.isCodeSent
                })
            }
        }
    },

    watch: {
        isCodeSending (newVal) {
            console.log('isCodeSending newVal = ', newVal)
        },

        isCodeSent (newVal) {
            console.log('isCodeSent newVal = ', newVal)
        }
    },

    computed: {
        phoneNumberErrors () {
            const errors = []

            if (!this.$v.form.phoneNumber.$dirty) return errors
            !this.$v.form.phoneNumber.required &&
                errors.push('Это поле обязательно для заполнения')

            return errors
        },

        passwordErrors () {
            const errors = []

            if (!this.$v.form.password.$dirty) return errors
            !this.$v.form.password.requiredIf &&
                errors.push('Это поле обязательно для заполнения')

            return errors
        },

        codeErrors () {
            const errors = []

            if (!this.$v.form.code.$dirty) return errors
            console.log('this.$v.form.code = ', this.$v.form.code.$dirty)
            !this.$v.form.code.requiredIf &&
                errors.push('Это поле обязательно для заполнения')

            return errors
        }
    },

    methods: {
        authorizeTelegram () {
            if (!this.checkFormValidation()) return

            if (!this.is2FA) {
                delete this.form.password
            }

            if (!this.form.phoneNumber && !this.form.password) {
                this.closeDialog()
            }

            this.$emit('authorize-telegram', this.form)

            this.$nextTick(() => {
                this.$v.$reset()
            })

            console.log('this.form = ', this.form)
        },

        closeDialog () {
            this.isDialogVisible = false
        },

        isNumber (e) {
            const regex = /[0-9]/
            if (!regex.test(e.key)) {
                e.returnValue = false
                if (e.preventDefault) e.preventDefault()
            }
        }
    },

    directives: {
        mask: VueMaskDirective
    }
}
</script>
