import { createApp } from 'vue';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faLinkedin, faTwitterSquare } from '@fortawesome/free-brands-svg-icons';
import { faAlignCenter, faAlignJustify, faAlignLeft, faAlignRight, faArrowDown, faArrowLeft, faArrowRight, faArrowUp, 
    faBold, faCircle, faExternalLinkAlt, faGripHorizontal, faItalic, faLink, faListOl, faListUl, faPaperPlane, faPencilAlt, faPlus, faPlusCircle, 
    faQuoteLeft, faRedo, faSquare, faStrikethrough, faTextHeight, faTrash, faTrashAlt, faUnderline, faUndo, faUnlink, faUserCircle } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon, FontAwesomeLayers, FontAwesomeLayersText } from '@fortawesome/vue-fontawesome';

import vueSuperCall from './utils/vue-util';
import VueSanitize from "vue-sanitize";
import Vuex from 'vuex/dist/vuex.global.js';


library.add(faAlignCenter, faAlignJustify, faAlignLeft, faAlignRight, faArrowDown, faArrowLeft, faArrowRight, faArrowUp,
    faBold, faCircle, faExternalLinkAlt, faGripHorizontal, faItalic, faLink, faLinkedin, faListOl, faListUl, faPaperPlane, faPencilAlt, faPlus, faPlusCircle,
    faQuoteLeft, faRedo, faSquare, faStrikethrough, faTextHeight, faTrash, faTrashAlt, faTwitterSquare, faUnderline, faUndo, faUnlink, faUserCircle);

const initVue = (mainComponent, el, data, store) => {
    const vueComponent = createApp(mainComponent, data)
        .component('font-awesome-icon', FontAwesomeIcon)
        .component('font-awesome-layers', FontAwesomeLayers)
        .component('font-awesome-layers-text', FontAwesomeLayersText)
        .mount(el);

    vueComponent.use(VueSanitize);
    vueComponent.use(store);
    vueComponent.prototype.$super = vueSuperCall;

    return vueComponent
}

export default initVue;