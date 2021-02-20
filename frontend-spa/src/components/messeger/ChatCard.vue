<template>
    <v-card
        :class="{ 'elevation-12': hover }"
        @mouseover="hover = true"
        @mouseleave="hover = false"
    >
        <v-list-item
            style="cursor: pointer"
        >
            <v-list-item-avatar
                class="pl-3"
                color="grey"
                size="60"
            >
                <span class="white--text headline">UN</span>

            </v-list-item-avatar>

            <div class="my-3 text-truncate">
                <v-list-item-title class="title">
                    User's nickname
                </v-list-item-title>

                <div class="d-flex align-center">
                    <svg-icon
                        icon-name="vk"
                        class="mr-1"
                        style="stroke: #2979FF"
                    />
                    <svg-icon
                        icon-name="telegram"
                        class="mr-1"
                        style="stroke: #212121"
                    />
                    <v-icon
                        color="success"
                        class="mr-1"
                    >
                        mdi-whatsapp
                    </v-icon>
                    <v-icon
                        color="warning"
                        class="mr-1"
                    >
                        mdi-at
                    </v-icon>
                    <svg-icon
                        icon-name="message"
                        style="stroke: #00ACC1"
                    />
                </div>

                <v-list-item-subtitle
                    class="mt-1 pb-1"
                >
                    Lorem ipsum dolor sit amet, consectetuer adipiscing
                    elit.dwqdwdq;qdlw pdwkqpd ldowq
                </v-list-item-subtitle>
            </div>
        </v-list-item>
    </v-card>
</template>

<script>
import SvgIcon from '@/components/common/SvgIcon'

export default {
    name: 'ChatCard',

    components: {
        SvgIcon
    },

    data: () => ({
        hover: false
    })
}
</script>
