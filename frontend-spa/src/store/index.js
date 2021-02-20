import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        currentUser: {}
    },

    mutations: {
        SET_CURRENT_USER (state, currentUser) {
            state.currentUser = currentUser
        }
    },

    actions: {
    },

    modules: {
    }
})
