import mitt from 'mitt';
import ProfilePage from './ProfilePage.vue';

const eventBus = mitt();

export {ProfilePage as page, eventBus};
