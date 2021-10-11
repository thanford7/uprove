import { createApp } from 'vue';
import { createStore } from 'vuex';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faLinkedin, faTwitterSquare } from '@fortawesome/free-brands-svg-icons';
import { faAlignCenter, faAlignJustify, faAlignLeft, faAlignRight, faArrowDown, faArrowLeft, faArrowRight, faArrowUp, 
    faBold, faCircle, faExternalLinkAlt, faGripHorizontal, faItalic, faLink, faListOl, faListUl, faPaperPlane, faPencilAlt, faPlus, faPlusCircle, 
    faQuoteLeft, faRedo, faSquare, faStrikethrough, faTextHeight, faTrash, faTrashAlt, faUnderline, faUndo, faUnlink, faUserCircle } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon, FontAwesomeLayers, FontAwesomeLayersText } from '@fortawesome/vue-fontawesome';

import vueSuperCall from './utils/vue-util';
import Vue3Sanitize from "vue-3-sanitize";

library.add(faAlignCenter, faAlignJustify, faAlignLeft, faAlignRight, faArrowDown, faArrowLeft, faArrowRight, faArrowUp,
    faBold, faCircle, faExternalLinkAlt, faGripHorizontal, faItalic, faLink, faLinkedin, faListOl, faListUl, faPaperPlane, faPencilAlt, faPlus, faPlusCircle,
    faQuoteLeft, faRedo, faSquare, faStrikethrough, faTextHeight, faTrash, faTrashAlt, faTwitterSquare, faUnderline, faUndo, faUnlink, faUserCircle);

const initVue = (mainComponent, el, data, eventBus) => {
    const store = createStore({
        state() {
            return {
                eventBus,
            }
        }
    });

    const vueComponent = createApp(mainComponent, data)
        .component('font-awesome-icon', FontAwesomeIcon)
        .component('font-awesome-layers', FontAwesomeLayers)
        .component('font-awesome-layers-text', FontAwesomeLayersText)
        .use(Vue3Sanitize)
        .use(store);

    vueComponent.mount(el);
    vueComponent.provide('$super', vueSuperCall);

    return vueComponent
}

export default initVue;