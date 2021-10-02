import { library } from '@fortawesome/fontawesome-svg-core';
import { faLinkedin, faTwitterSquare } from '@fortawesome/free-brands-svg-icons';
import { faAlignCenter, faAlignJustify, faAlignLeft, faAlignRight, faArrowDown, faArrowLeft, faArrowRight, faArrowUp, 
    faBold, faCircle, faExternalLinkAlt, faGripHorizontal, faItalic, faLink, faListOl, faListUl, faPaperPlane, faPencilAlt, faPlus, faPlusCircle, 
    faQuoteLeft, faRedo, faSquare, faStrikethrough, faTextHeight, faTrash, faTrashAlt, faUnderline, faUndo, faUnlink, faUserCircle } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon, FontAwesomeLayers, FontAwesomeLayersText } from '@fortawesome/vue-fontawesome';

import vueSuperCall from '../../utils/vue-util';
import Vue from 'vue/dist/vue.runtime.esm.js';
import VueSanitize from "vue-sanitize";

library.add(faAlignCenter, faAlignJustify, faAlignLeft, faAlignRight, faArrowDown, faArrowLeft, faArrowRight, faArrowUp, 
    faBold, faCircle, faExternalLinkAlt, faGripHorizontal, faItalic, faLink, faLinkedin, faListOl, faListUl, faPaperPlane, faPencilAlt, faPlus, faPlusCircle, 
    faQuoteLeft, faRedo, faSquare, faStrikethrough, faTextHeight, faTrash, faTrashAlt, faTwitterSquare, faUnderline, faUndo, faUnlink, faUserCircle);
Vue.component('font-awesome-icon', FontAwesomeIcon);
Vue.component('font-awesome-layers', FontAwesomeLayers);
Vue.component('font-awesome-layers-text', FontAwesomeLayersText);

Vue.use(VueSanitize);
Vue.use(Vuex);
Vue.prototype.$super = vueSuperCall;

export default Vue;