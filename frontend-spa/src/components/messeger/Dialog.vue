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
            :id="dialog.entity.id"
            :style="getChatHeight"
            class="overflow-y-auto overflow-x-hidden"
            @scroll="checkEndOfScroll"
        >

            <div
                v-for="(message, index) in messages"
                :key="index"
                class="my-2 mx-8 d-flex"
            >
                <message
                    :class="checkIfIAmSender(message.sender_id) ? 'ml-auto' : 'mr-auto'"
                    :message="message"
                    :am-i-sender="checkIfIAmSender(message.sender_id)"
                />
            </div>
        </div>

        <div
            v-if="!isChannel || hasAdminRights"
            class="mt-auto"
        >
            <div
                class="pa-0 ma-0"
            >
                <v-textarea
                    style="border-radius: 0; border-left: 1px solid #ccc; font-size: 18px;"
                    class="elevation-2 pt-n4"
                    solo
                    :state="validateState('message')"
                    hide-details
                    @keydown.enter.exact.prevent="sendMessage"
                    placeholder="Сообщение..."
                    auto-grow
                    row-height="9"
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
    </div>
</template>

<script>
import Message from '@/components/messeger/Message'
import { myValidationMixin } from '@/mixins/validationMixin'
import { required } from 'vuelidate/lib/validators'

export default {
    name: 'Dialog',

    mixins: [myValidationMixin],

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

        offset: 0,

        scrollTop: 0,

        hasAvatar: true,
    }),

    validations: {
        form: {
            message: { required }
        }
    },

    computed: {
        isChannel () {
            return this.dialog.entity.type === 'channel'
        },

        hasAdminRights () {
            return this.isChannel && this.dialog.entity.admin_rights
        },

        getChatHeight () {
            if (!this.isChannel || this.hasAdminRights) {
                return {
                    height: '87vh'
                }
            }

            return {
                height: '94vh'
            }
        }
    },

    methods: {
        checkIfIAmSender (/** @type {number} */ senderId) {
            return senderId === this.$store.state.currentUser.telegram_credentials.id
        },

        sendMessage () {
            if (!this.checkFormValidation()) return

            this.$emit('send-message', this.dialog.entity.id, this.form.message)

            this.form.message = ''
            this.$nextTick(() => {
                this.$v.$reset()
            })
        },

        checkEndOfScroll () {
            const dialog = document.getElementById(this.dialog.entity.id)

            if (dialog.scrollTop === 0) {
                this.offset = this.offset + 30
                this.$emit('load-more-messages', this.dialog, this.offset,
                    this.scrollTop)
            }
        }
    }
}
</script>
