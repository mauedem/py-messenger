<template>
    <v-navigation-drawer
        app
        class="pt-4 elevation-2"
        mini-variant-width="80"
        width="280"
        :mini-variant.sync="isNavigationOpen"
    >
        <v-list-item class="pl-2 pr-0">
            <v-avatar
                class="mr-3"
                color="black"
                size="60"
            >
                <span class="white--text headline">PM</span>
            </v-avatar>

            <div>
                <v-list-item-title class="title text-h5">
                    PyMessenger
                </v-list-item-title>
                <v-list-item-subtitle class="mt-1">
                    2021
                </v-list-item-subtitle>
            </div>

            <v-btn
                class="mr-3 ml-auto"
                icon
                @click.stop="toggleNavigationState"
            >
                <v-icon>mdi-chevron-left</v-icon>
            </v-btn>
        </v-list-item>

        <v-divider class="mt-3"/>

        <v-list-item class="d-flex align-center mt-3 pl-2 pr-0">
            <v-avatar
                class="mr-3"
                color="primary"
                size="60"
            >
                <span class="white--text headline">ED</span>
            </v-avatar>

            <div class="d-inline-block mr-auto">
                <p class="mb-0 font-weight-bold">Eryn Drem</p>
                <p class="mb-0">@eryndrem</p>
            </div>
        </v-list-item>

        <v-divider class="mt-3"/>

        <v-list
            class="navigation"
        >
            <v-list-item
                v-for="item in items"
                :key="item.title"
                link
            >
                <v-list-item-icon class="mr-3 ml-1">
                    <v-icon
                        style="font-size: 36px"
                        color="gray"
                    >
                        {{ item.icon }}
                    </v-icon>
                </v-list-item-icon>

                <v-list-item-content>
                    <v-list-item-title style="font-size: 14px">{{ item.title }}
                    </v-list-item-title>
                </v-list-item-content>
            </v-list-item>

            <v-list-item
                class="navigation__item mt-auto"
                style="margin-top: 440px !important;"
                @click="showConfirmLogoutModal"
                link
            >
                <v-list-item-icon class="mr-3 ml-1">
                    <v-icon
                        style="font-size: 36px"
                        color="gray"
                    >
                        mdi-logout-variant
                    </v-icon>
                </v-list-item-icon>

                <v-list-item-content>
                    <v-list-item-title style="font-size: 14px">Выход
                    </v-list-item-title>
                </v-list-item-content>
            </v-list-item>
        </v-list>
    </v-navigation-drawer>
</template>

<script>
export default {
    name: 'Navigation',

    data: () => ({
        isNavigationOpen: true,

        items: [
            { title: 'Мои учетные данные', icon: 'mdi-view-dashboard' },
            { title: 'Мои контакты', icon: 'mdi-forum' },
            { title: 'Настройки', icon: 'mdi-cog' }
        ]
    }),

    methods: {
        toggleNavigationState () {
            this.isNavigationOpen = !this.isNavigationOpen
        },

        showConfirmLogoutModal () {
            this.$emit('show-confirm-logout-modal')
        },
    }
}
</script>
