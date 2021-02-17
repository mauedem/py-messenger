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
                                label="Логин"
                                prepend-icon="mdi-account"
                            />

                            <v-text-field
                                v-model="form.password"
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
                        <span class="create-user-button">
                            Создать аккаунт
                        </span>
                    </v-btn>
                </div>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
export default {
    name: 'SignIn',

    data: () => ({
        form: {
            login: '',
            password: ''
        },

        isPasswordVisibe: false
    }),

    methods: {
        togglePasswordVisibility() {
            this.isPasswordVisibe = !this.isPasswordVisibe
        }
    }
}
</script>
