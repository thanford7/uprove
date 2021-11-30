import '../css/base.scss';
import 'bootstrap';
import 'selectize/dist/js/selectize.min.js';
import dayjs from "dayjs/esm";
import footer from './modules/pages/footer/footer.vue';
import header from './modules/pages/header/header.vue';
import initVue from './vueCommon';
import Pages from './mainPageLoader';
import $ from 'jquery';
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
    const {page} = Pages[pageName];
    initVue(page, '#vue-container');
    initVue(header, '#site-header .navbar');
    initVue(footer, '#site-footer');

    // Remove data scripts so it's not visible after data has been loaded in Vue
    $('#globalData').remove();
    $('#initData').remove();

    $('.modal').on('hide.bs.modal', (e) => {
        $(document.body).removeClass('modal-open');
        $('.modal-backdrop').remove();
    });
});

_.defer(() => $(window).trigger('resize-throttled'));
