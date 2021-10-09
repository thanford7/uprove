import FrontPage from './FrontPage.vue';
import initPage from '../../../scripts';
import Vue from 'vue';

initPage();

const eventBus = Vue.createApp({
    methods: {

    }
});

const store = new Vuex.Store({
    state() {
        return {
            eventBus: eventBus,
        }
    }
});

$(() => {
    Vue.createApp({
        el: '#vue-container',
        store,
        render(h){
            return h(FrontPage, {});
        }
    });
});