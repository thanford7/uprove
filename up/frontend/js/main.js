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
import Vue from 'vue';
import _ from 'lodash';

let jQueryConsole = false;
/* dev-only */
jQueryConsole = true;
/* end-dev-ony */
if (jQueryConsole) {
    window.$ = window.jQuery = $;
}

_.defer(() => {
    initVue();
    const pageName = $('body').data('page');
    const pageLoader = Pages[pageName];
    pageLoader(mainData);  // Load Vue for main body
    Vue.createApp(
        header,
        {postType: wpApi.postType, userId: parseInt(wpApi.userId)}
    ).mount('.site-header');
    Vue.createApp(footer, {postType: wpApi.postType}).mount('#site-footer');
});

_.defer(() => $(window).trigger('resize-throttled'));
