<template>
        <v-dialog
        v-model="isDialogVisible"
        max-width="350"
    >
        <template v-slot:activator="{ on, attrs }">
            <v-btn
                color="red"
                outlined
                v-bind="attrs"
                v-on="on"
            >
                Выйти
            </v-btn>
        </template>

        <v-card>
            <v-card-title>
                <span class="headline">Выход из Telegram</span>
            </v-card-title>

            <v-card-text class="text-center">
                Вы уверены, что хотите выйти из Telegram?
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
                    @click="logoutTelegram"
                >
                    Подтвердить
                </v-btn>
            </v-card-actions>

            <v-progress-linear
                :active="false"
                indeterminate
                absolute
                bottom
                color="deep-purple accent-4"
            ></v-progress-linear>
        </v-card>
    </v-dialog>
</template>

<script>
export default {
    name: 'LogoutTelegramModal',

    data: () => ({
        isDialogVisible: false
    }),

    methods: {
        closeDialog () {
            this.isDialogVisible = false
        },

        logoutTelegram () {
            this.closeDialog()

            this.$emit('logout-telegram')
        }
    }
}
</script>
