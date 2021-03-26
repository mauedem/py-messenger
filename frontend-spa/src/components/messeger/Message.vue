<template>
    <v-card
        :color="amISender ? myMessageColor : penfriendMessageColor"
        :style="getCardWidth"
        :class="amISender ? myMessageStyle : penfriendMessageStyle"
    >
        <div
            v-if="!message.media && message.text"
            class="d-flex flex-row align-end"
        >
            <v-card-text class="px-4 py-2">
                <span
                    :class="amISender ? myMessageTextColor : penfriendMessageTextColor"
                    style="font-size: 16px"
                >
                    {{ message.text }}
                </span>
            </v-card-text>

            <v-card-subtitle
                class="mb-2 mr-4"
                :class="amISender ? 'white--text' : ''"
            >
                {{ getMessageTime }}
            </v-card-subtitle>
        </div>

        <v-img
            v-show="isPhoto"
            v-else-if="message.media && !message.text"
            :src="`http://localhost/media/dialogs/${message.media}`"
            style="border-bottom-left-radius: 24px;
            border-bottom-right-radius: 24px"
            @error="isPhoto = false"
        >
            <div
                class="d-flex justify-end fill-height">
                <v-chip
                    class="d-inline-block text-center mt-auto mb-2 mr-3 px-2"
                    style="opacity: 0.7; height: 20px"
                    color="grey darken-4"
                >
                    <span
                        class="white--text"
                        style="z-index: 999"
                    >
                        {{ getMessageTime }}
                    </span>
                </v-chip>
            </div>
        </v-img>

        <div
            v-else-if="message.media && message.text"
        >
            <v-img
                :src="`http://localhost/media/dialogs/${message.media}`"
                style="border-top-left-radius: 24px;
                border-top-right-radius: 24px"
            >
            </v-img>

            <div class="d-flex flex-row align-end">
                <v-card-text class="px-4 py-2">
                    <span
                        :class="amISender ? myMessageTextColor : penfriendMessageTextColor"
                        style="font-size: 16px"
                    >
                        {{ message.text }}
                    </span>
                </v-card-text>

                <v-card-subtitle
                    class="mb-2 mr-4"
                    :class="amISender ? 'white--text' : ''"
                >
                    {{ getMessageTime }}
                </v-card-subtitle>
            </div>
        </div>
    </v-card>
</template>

<script>
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
        }
    }
}
</script>
