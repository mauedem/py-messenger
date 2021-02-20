<template>
    <v-row no-gutters>
        <v-col
            cols="4"
            class="pb-0"
        >
            <chats />
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
        noDialogSelected: true
    })
}
</script>
