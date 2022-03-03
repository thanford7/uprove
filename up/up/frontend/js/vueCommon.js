import {createApp} from 'vue';
import {ajaxRequestMixin, filterMixin, globalVarsMixin, modalsMixin, popoverMixin, store} from './vueMixins';
import Vue3Sanitize from "vue-3-sanitize";

const initVue = (mainComponent, el) => {
    const vueComponent = createApp(mainComponent)
        .use(Vue3Sanitize)
        .use(store)
        .mixin(popoverMixin)
        .mixin(ajaxRequestMixin)
        .mixin(globalVarsMixin)
        .mixin(modalsMixin)
        .mixin(filterMixin);

    vueComponent.mount(el);
    return vueComponent
}

export default initVue;