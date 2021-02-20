<template>
    <svg class="icon">
        <use :xlink:href="sprite + '#' + iconName"></use>
    </svg>
</template>

<script>
const requireAll = requireContext => requireContext.keys().map(requireContext)
const req = require.context('@/assets/', false, /\.svg$/)

export default {
    name: 'SvgIcon',

    props: {
        iconName: String
    },

    data () {
        return {
            sprite: requireAll(req)
        }
    }
}
</script>

