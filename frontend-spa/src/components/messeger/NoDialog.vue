<template>
    <div
        class="d-flex justify-center align-center"
        style="width: 100%; height: 100%"
    >
        <p
            v-if="!areMessagesLoading"
            class="text-h6 font-weight-regular"
            style="font-size: 14px"
        >
            <v-chip
                class="d-inline-block px-3"
                style="opacity: 0.7; height: 24px"
                color="grey darken-4"
            >
                <span
                    class="white--text"
                    style="z-index: 999; font-weight: bold"
                >
                    Чтобы начать, выберите чат
                </span>
            </v-chip>
        </p>

        <v-progress-circular
            v-else
            :size="70"
            :width="7"
            color="primary"
            indeterminate
        />
    </div>
</template>

<script>
export default {
    name: 'NoDialog',

    props: {
        areMessagesLoading: {
            type: Boolean,
            required: true
        }
    }
}
</script>
