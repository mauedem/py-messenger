<template>
    <div
        style="height: 100vh"
        class="overflow-y-hidden d-flex flex-column"
    >
        <v-toolbar
            color="white"
            light
            outlined
            style="border-left: 1px solid #ccc !important; z-index: 2"
            class="elevation-2"
            max-height="64px"
        >
            <v-avatar
                size="40"
                color="primary"
            >

                <v-img
                    v-if="hasAvatar"
                    :src="`http://localhost/media/avatars/${dialog.entity.avatar_id}`"
                    @error="hasAvatar = false"
                />
                <span
                    v-else
                    class="headline mx-auto"
                    style="color: white"
                >
                    {{ dialog.name[0].toUpperCase() }}
                </span>
            </v-avatar>

            <v-toolbar-title class="ml-4">
                <span style="color: black">{{ dialog.name }}</span>
            </v-toolbar-title>

            <v-spacer></v-spacer>
            <v-btn
                icon
                color="primary"
            >
                <v-icon>mdi-magnify</v-icon>
            </v-btn>
            <v-btn
                icon
                color="primary"
            >
                <v-icon>mdi-heart</v-icon>
            </v-btn>
            <v-btn
                icon
                color="primary"
            >
                <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
        </v-toolbar>

        <div
            style="height: 87vh"
            class="overflow-y-auto overflow-x-hidden"
        >
<!--            <div class="d-flex justify-center">-->
<!--                <v-chip-->
<!--                    class="my-3 text-center"-->
<!--                    style="opacity: 0.8"-->
<!--                    color="grey darken-4"-->
<!--                >-->
<!--                    <span class="white&#45;&#45;text">{{ messagesDate }}</span>-->
<!--                </v-chip>-->
<!--            </div>-->

            <div
                v-for="message in messages"
                :key="message.id"
                class="my-2 mx-8 d-flex"
            >
                <message
                    :class="checkIfIAmSender(message.sender_id) ? 'ml-auto' : 'mr-auto'"
                    :message="message"
                    :am-i-sender="checkIfIAmSender(message.sender_id)"
                />
            </div>
        </div>

        <div class="mt-auto">
            <v-textarea
                style="border-radius: 0; border-left: 1px solid #ccc;
                font-size: 18px"
                class="elevation-2 pt-n4"
                row-height="9"
                solo
                hide-details
                placeholder="Сообщение..."
                auto-grow
                v-model="form.message"
            >
                <template #prepend-inner>
                    <v-file-input
                        dense
                        hide-details
                        class="mt-n3"
                        hide-input
                        accept="image/*"
                    />
                </template>
            </v-textarea>
        </div>
    </div>
</template>

<script>
import Message from '@/components/messeger/Message'
// import moment from 'moment'
import 'moment/locale/ru'

export default {
    name: 'Dialog',

    components: {
        Message
    },

    props: {
        dialog: {
            type: Object,
            required: false
        },

        messages: {
            type: Array,
            required: true
        }
    },

    data: () => ({
        form: {
            message: ''
        },

        hasAvatar: true
    }),

    methods: {
        checkIfIAmSender (/** @type {number} */ senderId) {
            return senderId === this.$store.state.currentUser.telegram_credentials.id
        },

        // getMessageDate (messageDate) {
        //     const dateWithoutTime = messageDate.substr(0, 10)
        //     moment.locale('ru')
        //
        //     const formattedDate = moment(dateWithoutTime, 'DD.MM.YYYY').format('DD MMMM')
        //
        //     if (this.messagesDate !== formattedDate) {
        //         this.messagesDate = formattedDate
        //     }
        //
        //     return formattedDate
        // }
    }
}
</script>
