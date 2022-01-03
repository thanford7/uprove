import '../css/base.scss';
import 'bootstrap';
import footer from './modules/pages/footer/footer.vue';
import header from './modules/pages/header/header.vue';
import initSelectize from "./customSelectize";
import initVue from './vueCommon';
import Pages from './mainPageLoader';
import 'jquery';

let jQueryConsole = false;
/* dev-only */
jQueryConsole = true;
/* end-dev-ony */
if (jQueryConsole) {
    window.$ = window.jQuery = $;
}

setTimeout(() => {
    const pageName = $('body').data('page');
    const {page, banner} = Pages[pageName];
    initSelectize();
    if (banner) {
        initVue(banner, '#hero');
    }
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
}, 1);

setTimeout(() => $(window).trigger('resize-throttled'), 1);
