import mitt from 'mitt';
import PrivacyPage from './PrivacyPage.vue';

const eventBus = mitt();

export {PrivacyPage as page, eventBus};