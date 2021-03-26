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
            Чтобы начать, выберите чат
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
    },

    watch: {
        areMessagesLoading (newVal) {
            console.log('areMessagesLoading NoDialog = ', newVal)
        }
    }
}
</script>
