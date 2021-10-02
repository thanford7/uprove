<template>
    <BaseModal
        modalId="editMediaModal"
        :modalTitle="`Edit ${contentItem.post_type}`"
        :isLargeDisplay="true"
        @saveChange="saveChange"
    >
        <MediaFormContent 
            v-if="contentItem" 
            ref="form"
            :contentItem="contentItem"
            :contentType="contentItem.post_type"
            :allowedBannerMediaTypes="allowedBannerMediaTypes"
        />
    </BaseModal>
</template>
<script>
import Modal from 'bootstrap/js/dist/modal';
import {mapState} from 'vuex';
import BaseModal from './BaseModal.vue';
import MediaFormContent from './MediaFormContent.vue';

export default {
    extends: BaseModal,
    data() {
        return {
            modal$: null,
            contentId: null,
        }
    },
    inheritAttrs: false,
    components: {BaseModal, MediaFormContent},
    computed: {
        ...mapState({
            eventBus: 'eventBus',
            contentItem(state) {
                return (this.contentId) ? state.content[this.contentId] : {}
            },
            crudUrl(state) {
                return `${state.crudBase}${this.contentItem.post_type}/${this.contentId}`
            }
        }),
        allowedBannerMediaTypes() {
            return (this.contentItem.post_type === 'video') ? ['video'] : ['video', 'image'];
        }
    },
    methods: {
        readForm() {
            return {}; // Form data is returned in getPreSaveChange
        },
        onSaveSuccess(requestData, responseData) {
            this.eventBus.loadContent([this.contentItem.post_type]);
        },
        hookEvents() {
            this.eventBus.$on('open:editMediaModal', (contentId) => {
                this.contentId = contentId;
                this.modal$.show();
            });
        },
        getPreSaveChange() {
            return this.$refs.form.getPreSaveChange();
        },
    },
    mounted() {
        if (!this.modal$) {
            this.modal$ = new Modal($('#editMediaModal'));
        }
    }
}
</script>