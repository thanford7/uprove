import ContactPage from "./ContactPage.vue";
import mitt from 'mitt';

const eventBus = mitt();

export {ContactPage as page, eventBus};