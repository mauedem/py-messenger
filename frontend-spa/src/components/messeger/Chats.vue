<template>
    <div
        class="elevation-4 overflow-y-auto"
        style="height: 100vh"
    >
        <v-form class="pt-5 mx-4 mb-n7">
            <v-text-field
                outlined
                height="20"
                placeholder="Search"
            >

            </v-text-field>
        </v-form>

        <div
            v-if="areDialodsLoading"
            class="mt-5 d-flex flex-column align-center"
        >
            <p class="text-h6 font-weight-regular">
                Получаем диалоги
            </p>

            <v-progress-linear
                style="width: 300px"
                :active="areDialodsLoading"
                indeterminate
                top
                color="deep-purple accent-4"
            />
        </div>

        <div
            v-show="!areDialodsLoading && !dialogs"
            class="mt-5"
        >
            <p class="text-h6 font-weight-regular text-center">
                Диалогов еще нет
            </p>

            <p class="text-center text--secondary body-2 mx-3">
                Чтобы добавить диалоги необходимо авторизоваться в одном
                из представленных мессенджеров. Перейдите в "Мои учетные
                данные", чтобы сделать это.
            </p>
        </div>

        <v-list
            two-line
        >
            <v-list-item-group
                v-model="selectedChat"
                color="primary"
            >
                <template v-for="(dialog, index) in dialogs">
                    <chat-card
                        :dialog="dialog"
                        :key="index"
                    />
                </template>
            </v-list-item-group>
        </v-list>
    </div>
</template>

<script>
import ChatCard from '@/components/messeger/ChatCard'

export default {
    name: 'Chats',

    components: {
        ChatCard
    },

    props: {
        areDialodsLoading: {
            type: Boolean,
            default: false
        },

        dialogs: {
            type: Array,
            required: false
        }
    },

    data: () => ({
        selectedChat: null
    })
}
</script>
