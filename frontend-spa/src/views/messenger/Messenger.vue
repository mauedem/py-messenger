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
                @send-message="sendMessage"
                @load-more-messages="getChatMessages"
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

        hasOffeset: false,

        scrollTop: 0,

        selectedChat: null,
        chatMessages: []
    }),

    watch: {
        chatMessages () {
            if (!this.hasOffeset) {
                setTimeout(() => {
                    this.scrollToEnd()
                }, 50)
            } else {
                this.preventScroll()
            }
        },
    },

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

        async getChatMessages (
            /** @type {object} */ dialog,
            /** @type {number} */ offset = 0,
            /** @type {number} */ scrollTop = 0
        ) {
            this.hasOffeset = offset !== 0

            this.scrollTop = scrollTop

            // TODO вынести это в отдельную ф-ию
            if (this.selectedChat?.entity.id === dialog.entity.id && offset === 0) {
                this.scrollToEnd()
                return
            }

            this.selectedChat = dialog
            this.noDialogSelected = false

            try {
                if (!this.hasOffeset) {
                    this.areMessagesLoading = true
                    this.chatMessages = []
                }

                const messages = await this.$transport.getDialogMessages(
                    dialog.entity.id,
                    dialog.entity.username,
                    offset
                )

                // TODO прерывать получение предыдущих сообщений при переключении диалога
                if (!this.chatMessages.length || offset === 0) {
                    this.chatMessages = messages
                } else {
                    this.chatMessages = [...messages, ...this.chatMessages]
                }
            } catch (err) {
                console.log(err)
            } finally {
                this.areMessagesLoading = false
            }
        },

        async sendMessage (
            /** @type {number} */ receiverId,
            /** @type {string} */ message
        ) {
            try {
                const sentMessage = await this.$transport.sendMessage({
                    receiver_id: receiverId,
                    message: message
                })
                this.chatMessages.push(sentMessage)
            } catch (err) {
                console.log('err = ', err)
            }
        },

        scrollToEnd () {
            const dialog = document.getElementById(this.selectedChat?.entity.id)
            dialog.scrollTop = dialog.scrollHeight - dialog.clientHeight
        },

        preventScroll () {
            // TODO пофиксить заглушку
            const dialog = document.getElementById(this.selectedChat.entity.id)
            dialog.scrollTop = this.scrollTop * 2
        }
    },

    // created () {
    //     if (this.$store.state.currentUser.telegram_credentials) {
    //         this.getTelegramDialogs()
    //     }
    // }
}
</script>
