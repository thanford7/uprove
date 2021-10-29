import mitt from 'mitt';
import TermsOfServicePage from "./TermsOfServicePage.vue";

const eventBus = mitt();

export {TermsOfServicePage as page, eventBus};