import FrontPage from './FrontPage.vue';
import initPage from '../../../scripts';
import Vue from '../vueCommon.js';

initPage();

const eventBus = new Vue({
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
    new Vue({
        el: '#vue-container',
        store,
        render(h){
            return h(FrontPage, {});
        }
    });
});