<template>
    <v-navigation-drawer
        app
        class="elevation-2"
        :class="isNavigationOpen ? 'pt-5' : 'pt-4'"
        mini-variant-width="80"
        width="280"
        height="100%"
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
                <v-list-item-subtitle class="pt-1">
                    Universal messaging <br> application
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

<!--        <v-divider class="mt-3"/>-->

        <v-list-item class="d-flex align-center mt-3 pl-2 pr-0">
            <v-avatar
                class="mr-3"
                color="primary"
                size="60"
            >
                <span class="white--text headline">ED</span>
            </v-avatar>

            <div class="d-inline-block mr-auto">
                <p class="mb-0 font-weight-bold">{{ currentUser.nickname }}</p>
                <p class="mb-0">@{{ currentUser.username }}</p>
            </div>
        </v-list-item>

        <v-divider class="mt-3"/>

        <v-list
            nav
            class="navigation"
        >
            <v-list-item-group v-model="selectedItem"
                               color="primary">
                <v-list-item
                    v-for="item in items"
                    :key="item.title"
                    @click="redirectToRouteName(item)"
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
                        <v-list-item-title style="font-size: 14px">
                            {{ item.title }}
                        </v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list-item-group>
        </v-list>

        <template v-slot:append>
            <v-list-item
                class="navigation__item mt-auto mb-2"
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
        </template>
    </v-navigation-drawer>
</template>

<script>
export default {
    name: 'Navigation',

    props: {
        user: {
            type: Object,
            required: true
        }
    },

    data: () => ({
        isNavigationOpen: true,

        selectedItem: 0,

        items: [
            {
                title: 'Мои чаты',
                icon: 'mdi-forum',
                routeName: 'Messenger'
            },
            {
                title: 'Мои учетные данные',
                icon: 'mdi-view-dashboard',
                routeName: 'Credentials'
            },
            { title: 'Настройки', icon: 'mdi-cog' }
        ]
    }),

    computed: {
        currentUser () {
            return this.$store.state.currentUser
        }
    },

    methods: {
        toggleNavigationState () {
            this.isNavigationOpen = !this.isNavigationOpen
        },

        showConfirmLogoutModal () {
            this.$emit('show-confirm-logout-modal')
        },

        redirectToRouteName (item) {
            this.selectedItem = item
            this.$router.push({ name: item.routeName })
        }
    }
}
</script>
