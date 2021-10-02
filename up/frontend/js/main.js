import 'bootstrap';
import header from './modules/pages/header/header.vue';
import footer from './modules/pages/footer/footer.vue';
import 'selectize/dist/js/selectize.min.js';
import 'jquery';
import Vue from './modules/pages/vueCommon';
import 'webpack-jquery-ui/draggable';
import 'webpack-jquery-ui/droppable';
import "../css/base.scss";

const initPage = () => {
  $(() => {
      new Vue({
          el: '.site-header',
          render(h){
              return h(header, {props: {postType: wpApi.postType, userId: parseInt(wpApi.userId)}});
          }
      });
      new Vue({
          el: '#site-footer',
          render(h){
              return h(footer, {props: {postType: wpApi.postType}});
          }
      });
  });
}

export default initPage;