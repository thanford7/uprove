import 'bootstrap';
import header from './modules/pages/header/header.vue';
import footer from './modules/pages/footer/footer.vue';
import 'selectize/dist/js/selectize.min.js';
import $ from 'jquery';
import initVue from './vueCommon';
import dayjs from "dayjs/esm";
import '../css/base.scss';
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
    const {page} = Pages[pageName];
    initVue(page, '#vue-container', );
    initVue(header, '#site-header .navbar');
    initVue(footer, '#site-footer');

    // Remove globalData script so it's not visible after data has been loaded in Vue
    $('#globalData').remove();
    $('#initData').remove();

    $('.modal').on('hide.bs.modal', (e) => {
        $(document.body).removeClass('modal-open');
        $('.modal-backdrop').remove();
    });
});

_.defer(() => $(window).trigger('resize-throttled'));
