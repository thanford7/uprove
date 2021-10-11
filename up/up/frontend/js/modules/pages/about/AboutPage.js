import AboutPage from './AboutPage.vue';
import mitt from "mitt";

const eventBus = mitt();

export {AboutPage as page, eventBus};