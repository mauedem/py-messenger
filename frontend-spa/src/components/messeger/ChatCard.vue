<template>
    <div>
        <v-divider
            :inset="true"
        ></v-divider>

        <v-list-item class="d-flex align-center">
            <v-list-item-avatar
                size="60"
                color="primary"
            >
                <v-img
                    v-if="hasAvatar"
                    :src="`http://localhost/media/avatars/${dialog.entity.avatar_id}`"
                    @error="hasAvatar = false"
                />
                <span
                    v-else
                    class="white--text headline mx-auto"
                >
                    {{ dialog.name[0].toUpperCase() }}
                </span>
            </v-list-item-avatar>

            <v-list-item-content>
                <v-list-item-title
                    class="ml-2 d-flex"
                    style="font-size: 18px"
                >
                    <span class="text-truncate">{{ dialog.name }}</span>

                    <div
                        class="d-inline-block ml-auto"
                        style="font-size: 16px"
                    >
                        {{ dialog.message.created_at }}
                    </div>
                </v-list-item-title>

                <div class="d-flex align-center">
                    <v-tooltip
                        color="grey darken-4"
                        top
                    >
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn
                                icon
                                v-bind="attrs"
                                v-on="on"
                            >
                                <svg-icon
                                    icon-name="telegram"
                                    style="stroke: #212121"
                                />
                            </v-btn>
                        </template>
                        <span>Вы можете написать этому <br> пользователю в
                            Telegram</span>
                    </v-tooltip>

                    <!-- VK style="stroke: #2979FF"-->
                    <v-tooltip
                        color="#757575"
                        top
                    >
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn
                                icon
                                v-bind="attrs"
                                v-on="on"
                            >
                                <svg-icon
                                    icon-name="vk"
                                    style="stroke: #999999"
                                />
                            </v-btn>
                        </template>
                        <span>Авторизуйтесь в VK, чтобы <br> написать этому
                            пользователю</span>
                    </v-tooltip>

                    <!-- Whatsapp color="success" -->
                    <v-tooltip
                        color="#757575"
                        top
                    >
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn
                                icon
                                v-bind="attrs"
                                v-on="on"
                            >
                                <v-icon
                                    style="color: #999999"
                                >
                                    mdi-whatsapp
                                </v-icon>
                            </v-btn>
                        </template>
                        <span>Авторизуйтесь в WhatsApp, чтобы <br> написать
                            этому пользователю</span>
                    </v-tooltip>

                    <!-- Email color="warning"-->
                    <v-tooltip
                        color="#757575"
                        top
                    >
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn
                                icon
                                v-bind="attrs"
                                v-on="on"
                            >
                                <v-icon
                                    style="color: #999999"
                                >
                                    mdi-at
                                </v-icon>
                            </v-btn>
                        </template>
                        <span>Авторизуйтесь в почте, чтобы <br> написать
                            этому пользователю</span>
                    </v-tooltip>

                    <!-- Message style="stroke: #00ACC1" -->
                    <v-tooltip
                        color="#757575"
                        top
                    >
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn
                                icon
                                v-bind="attrs"
                                v-on="on"
                            >
                                <svg-icon
                                    icon-name="message"
                                    style="stroke: #999999"
                                />
                            </v-btn>
                        </template>
                        <span>Наш мессенджер пока недоступен :)</span>
                    </v-tooltip>
                </div>

                <!-- TODO чекать медиа в сообщении -->
                <v-list-item-subtitle
                    class="text-truncate ml-2"
                >
                    {{ dialog.message.text }}
                </v-list-item-subtitle>
            </v-list-item-content>
        </v-list-item>
    </div>
</template>

<script>
import SvgIcon from '@/components/common/SvgIcon'

export default {
    name: 'ChatCard',

    components: {
        SvgIcon
    },

    props: {
        dialog: {
            type: Object,
            required: true
        }
    },

    data: () => ({
        hasAvatar: true
    })
}
</script>
