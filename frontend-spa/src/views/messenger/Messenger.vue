<template>
    <v-row no-gutters>
        <v-col
            cols="4"
            class="pb-0"
        >
            <chats
                :are-dialods-loading="areDialogsLoading"
                :dialogs="dialogs"
            />
        </v-col>

        <v-col
            v-if="noDialogSelected"
            cols="8"
        >
            <no-dialog />
        </v-col>

        <v-col
            v-else
            cols="8"
        >
            <dialogs />
        </v-col>
    </v-row>
</template>

<script>
import Chats from '@/components/messeger/Chats'
import NoDialog from '@/components/messeger/NoDialog'
import Dialogs from '@/components/messeger/Dialogs'

export default {
    name: 'Messenger',

    components: {
        Chats,
        NoDialog,
        Dialogs
    },

    data: () => ({
        noDialogSelected: true,

        areDialogsLoading: false,

        dialogs: []
    }),

    methods: {
        async getTelegramDialogs () {
            try {
                this.areDialogsLoading = true

                const dialogs = await this.$transport.getTelegramDialogs()
                console.log('dialogs = ', dialogs)
                this.dialogs = dialogs[0]
            } catch (err) {
                const { message } = err
                console.log(message)
            } finally {
                this.areDialogsLoading = false
            }
        }
    },

    created () {
        this.getTelegramDialogs()
    }
}
</script>
