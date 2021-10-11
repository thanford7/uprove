import { createApp } from 'vue';
import 'bootstrap';
import header from './modules/pages/header/header.vue';
import footer from './modules/pages/footer/footer.vue';
import 'selectize/dist/js/selectize.min.js';
import $ from 'jquery';
import initVue from './vueCommon';
import dayjs from "dayjs/esm";
import '../css/base.scss';
import mainData from './mainData';
import Pages from './mainPageLoader';
import _ from 'lodash';

let jQueryConsole = false;
/* dev-only */
jQueryConsole = true;
/* end-dev-ony */
if (jQueryConsole) {
    window.$ = window.jQuery = $;
}

_.defer(() => {
    const pageName = $('body').data('page');
    const {page, eventBus} = Pages[pageName];
    initVue(page, '#vue-container', mainData, eventBus);
    createApp(
        header,
        {postType: null, userId: 0}
    ).mount('.site-header');
    createApp(footer, {postType: null}).mount('#site-footer');
});

_.defer(() => $(window).trigger('resize-throttled'));
