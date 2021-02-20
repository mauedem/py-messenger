<template>
    <div class="elevation-4"
         style="height: 100vh">
        <v-form class="pt-5 mx-4 mb-n7">
            <v-text-field
                outlined
                height="20"
                placeholder="Search"
            >

            </v-text-field>
        </v-form>

        <v-list class="mt-0 overflow-y-auto">
            <chat-card
                v-for="i in 3"
                :key="i"
                class="mb-2 mt-1"
            />
        </v-list>
    </div>
</template>

<script>
import ChatCard from '@/components/messeger/ChatCard'

export default {
    name: 'Chats',

    components: {
        ChatCard
    }
}
</script>
