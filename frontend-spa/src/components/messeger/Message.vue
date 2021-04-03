<template>
    <v-card
        class="message"
        :color="amISender ? myMessageColor : penfriendMessageColor"
        :style="getCardWidth"
        :class="amISender ? myMessageStyle : penfriendMessageStyle"
    >
        <div
            v-if="!message.media && message.text"
            class="d-flex flex-row align-end"
        >
            <v-card-text
                class="px-4 py-2"
                style="white-space: pre-wrap"
            >
                <span
                    :class="amISender ? myMessageTextColor : penfriendMessageTextColor"
                    style="font-size: 16px"
                    v-text="message.text"
                >
                </span>
            </v-card-text>

            <v-tooltip top>
                <template v-slot:activator="{ on, attrs }">
                    <v-card-subtitle
                        class="mr-4 py-2"
                        :class="amISender ? 'white--text' : ''"
                        v-bind="attrs"
                        v-on="on"
                    >
                        {{ getMessageTime }}
                    </v-card-subtitle>
                </template>
                <span>{{ getMessageDate }}</span>
            </v-tooltip>
        </div>

        <v-dialog
            v-else-if="message.media && !message.text"
            max-width="900px"
        >
            <template v-slot:activator="{ on, attrs }">
                <v-img
                    v-show="isPhoto"
                    :src="`http://localhost/media/dialogs/${message.media}`"
                    style="border-bottom-left-radius: 24px;
                    border-bottom-right-radius: 24px;"
                    @error="isPhoto = false"
                    v-bind="attrs"
                    v-on="on"
                >
                    <div
                        class="d-flex justify-end fill-height">
                        <v-tooltip top>
                            <template v-slot:activator="{ on, attrs }">
                                <v-chip
                                    class="d-inline-block text-center mt-auto mb-2 mr-3 px-2"
                                    style="opacity: 0.7; height: 20px"
                                    color="grey darken-4"
                                    v-bind="attrs"
                                    v-on="on"
                                >
                                    <span
                                        class="white--text"
                                        style="z-index: 999"
                                    >
                                        {{ getMessageTime }}
                                    </span>
                                </v-chip>
                            </template>
                            <span>{{ getMessageDate }}</span>
                        </v-tooltip>
                    </div>
                </v-img>
            </template>

            <v-img
                v-show="isPhoto"
                :src="`http://localhost/media/dialogs/${message.media}`"
                @error="isPhoto = false"
                max-height="100%"
                width="100%"
            >
                <div
                    class="d-flex justify-end fill-height">
                    <v-tooltip top>
                        <template v-slot:activator="{ on, attrs }">
                            <v-chip
                                class="d-inline-block text-center mt-auto mb-2 mr-3 px-2"
                                style="opacity: 0.7; height: 20px"
                                color="grey darken-4"
                                v-bind="attrs"
                                v-on="on"
                            >
                        <span
                            class="white--text"
                            style="z-index: 999"
                        >
                            {{ getMessageTime }}
                        </span>
                            </v-chip>
                        </template>
                        <span>{{ getMessageDate }}</span>
                    </v-tooltip>
                </div>
            </v-img>
        </v-dialog>

        <div
            v-else-if="message.media && message.text"
        >
            <div class="d-flex flex-row align-end">
                <v-card-text class="px-4 py-2"
                             style="white-space: pre-wrap">
                    <span
                        :class="amISender ? myMessageTextColor : penfriendMessageTextColor"
                        style="font-size: 16px"
                        v-text="message.text"
                    >
                    </span>
                </v-card-text>

                <v-tooltip top>
                    <template v-slot:activator="{ on, attrs }">
                        <v-card-subtitle
                            class="mr-4 py-2"
                            :class="amISender ? 'white--text' : ''"
                            v-bind="attrs"
                            v-on="on"
                        >
                            {{ getMessageTime }}
                        </v-card-subtitle>
                    </template>
                    <span>{{ getMessageDate }}</span>
                </v-tooltip>
            </div>

            <v-dialog max-width="900px">
                <template v-slot:activator="{ on, attrs }">
                    <v-img
                        :src="`http://localhost/media/dialogs/${message.media}`"
                        style="border-bottom-left-radius: 24px;
                        border-bottom-right-radius: 24px;"
                        v-bind="attrs"
                        v-on="on"
                    >
                    </v-img>
                </template>

                <v-img
                    :src="`http://localhost/media/dialogs/${message.media}`"
                >
                </v-img>
            </v-dialog>
        </div>
    </v-card>
</template>

<script>
import moment from 'moment'
import 'moment/locale/ru'

export default {
    name: 'Message',

    props: {
        message: {
            type: Object,
            required: true
        },

        amISender: {
            type: Boolean,
            default: false
        }
    },

    data: () => ({
        penfriendMessageStyle: {
            'rounded-r-xl': true,
            'rounded-tl-xl': true
        },
        penfriendMessageColor: 'grey lighten-4',
        penfriendMessageTextColor: {
            'black--text': true
        },

        myMessageStyle: {
            'rounded-l-xl': true,
            'rounded-tr-xl': true
        },
        myMessageColor: 'primary',
        myMessageTextColor: {
            'white--text': true
        },

        // TODO сделать отображение документов
        isPhoto: true
    }),

    computed: {
        getMessageTime () {
            return this.message.created_at.substring(12)
        },

        getCardWidth () {
            if (!this.message.media && this.message.text) {
                return {
                    width: 'auto',
                    'max-width': '80%'
                }
            }

            return {
                width: 'auto',
                'max-width': '40%'
            }
        },

        getMessageDate () {
            const messageDate = this.message.created_at.toString()

            const dateWithoutTime = messageDate.substr(0, 10)
            moment.locale('ru')

            return moment(dateWithoutTime, 'DD.MM.YYYY').format('DD MMMM')
        }
    }
}
</script>
