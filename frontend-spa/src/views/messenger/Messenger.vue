<template>
    <v-row no-gutters>
        <v-col
            cols="4"
            class="pb-0"
        >
            <chats
                @get-telegram-dialogs="getTelegramDialogs"
                :are-dialods-loading="areDialogsLoading"
                :dialogs="dialogs"
                @select-chat="getChatMessages"
            />
        </v-col>

        <v-col
            v-if="noDialogSelected || areMessagesLoading"
            cols="8"
        >
            <no-dialog :are-messages-loading="areMessagesLoading" />
        </v-col>

        <v-col
            v-else
            cols="8"
        >
            <Dialog
                :dialog="selectedChat"
                :messages="chatMessages"
            />
        </v-col>
    </v-row>
</template>

<script>
import Chats from '@/components/messeger/Chats'
import NoDialog from '@/components/messeger/NoDialog'
import Dialog from '@/components/messeger/Dialog'

export default {
    name: 'Messenger',

    components: {
        Chats,
        NoDialog,
        Dialog
    },

    data: () => ({
        noDialogSelected: true,

        areDialogsLoading: false,
        areMessagesLoading: false,

        dialogs: [],

        selectedChat: null,
        chatMessages: []
    }),

    methods: {
        async getTelegramDialogs () {
            try {
                this.areDialogsLoading = true

                const dialogs = await this.$transport.getTelegramDialogs()
                this.dialogs = dialogs[0]
            } catch (err) {
                const { message } = err
                console.log(message)
            } finally {
                this.areDialogsLoading = false
            }
        },

        async getChatMessages (/** @type {object} */ dialog) {
            this.selectedChat = dialog
            this.noDialogSelected = false

            try {
                this.areMessagesLoading = true

                this.chatMessages = await this.$transport.getDialogMessages(dialog.entity.id)
            } catch (err) {
                console.log(err)
            } finally {
                this.areMessagesLoading = false
            }
        }
    },

    // created () {
    //     this.getTelegramDialogs()
    // }
}
</script>
