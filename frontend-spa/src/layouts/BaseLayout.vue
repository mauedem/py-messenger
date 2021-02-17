<template>
    <div>
        <v-navigation-drawer
              app
              class="pt-4"
              color="grey lighten-3"
              mini-variant>

            <v-avatar
                v-for="n in 6"
                :key="n"
                :color="`grey ${n === 1 ? 'darken' : 'lighten'}-1`"
                :size="n === 1 ? 36 : 20"
                class="d-block text-center mx-auto mb-9" />
        </v-navigation-drawer>

        <v-main>
            <slot></slot>
        </v-main>
    </div>
</template>

<script>
export default {
    name: 'BaseLayout'
}
</script>
