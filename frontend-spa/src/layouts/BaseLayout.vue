<template>
    <div>
        <navigation />

        <v-main>
            <slot></slot>
        </v-main>
    </div>
</template>

<script>
import Navigation from '@/components/Navigation'

export default {
    name: 'BaseLayout',

    components: {
        Navigation
    }
}
</script>
