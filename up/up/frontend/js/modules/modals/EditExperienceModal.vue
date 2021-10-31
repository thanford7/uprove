<template>
    <BaseModal
        :modalId="modalName"
        modalTitle="Edit experience"
        :isLargeDisplay="true"
        @saveChange="saveChange"
    >
        <ExperienceFormContent ref="form" :contentItem="contentItem"/>
    </BaseModal>
</template>
<script>
import Modal from 'bootstrap/js/dist/modal';
import {mapState} from 'vuex';
import BaseModal from './BaseModal.vue';
import ExperienceFormContent from './ExperienceFormContent.vue';

export default {
    extends: BaseModal,
    data() {
        return {
            modalName: 'editExperienceModal',
            contentId: null,
        }
    },
    inheritAttrs: false,
    components: {BaseModal, ExperienceFormContent},
    computed: {
        ...mapState({
            contentItem(state) {
                return (this.contentId) ? state.content[this.contentId] : {}
            },
            crudUrl(state) {
                return `${state.crudBase}experience/${this.contentId}`
            }
        })
    },
    methods: {
        readForm() {
            return {};  // Form data is retrieved in getPreSaveChange
        },
        onSaveSuccess(requestData, responseData) {
            this.eventBus.loadContent(['experience'])
        },
        hookEvents() {
            this.eventBus.$on('open:editExperienceModal', (contentId) => {
                this.contentId = contentId;
                this.modal$.show();
            });
        },
        getPreSaveChange() {
            return this.$refs.form.getPreSaveChange();
        },
    },
}
</script>