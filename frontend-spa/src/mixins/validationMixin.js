import { validationMixin } from 'vuelidate';

export const myValidationMixin = {
    mixins: [validationMixin],

    methods: {
        validateState (value) {
            const { $dirty, $error } = this.$v.form[value]
            return $dirty ? !$error : null
        },

        checkFormValidation () {
            this.$v.$touch()

            return !this.$v.$invalid
        },
    }
}
