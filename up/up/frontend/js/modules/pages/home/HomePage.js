import HomePage from './HomePage.vue';
import mitt from 'mitt';

const eventBus = mitt();

export {HomePage as page, eventBus};