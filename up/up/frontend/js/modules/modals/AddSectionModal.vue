<template>
    <BaseModal
        :modalId="modalName"
        modalTitle="Add section"
        :isLargeDisplay="true"
        @saveChange="saveChange"
    >
        <div class="mb-3">
            <label :for="`addSectionTitle`" class="form-label">Section title</label>
            <InputSelectize :cfg="addSectionCfg" placeholder="Add or select a new section title" @selected="formData.title = $event"/>
        </div>
    </BaseModal>
</template>
<script>
import {mapState} from 'vuex';
import BaseModal from './BaseModal.vue';
import dataUtil from '../../utils/data';
import InputSelectize from '../inputs/InputSelectize.vue';

export default {
    extends: BaseModal,
    components: {BaseModal, InputSelectize},
    inheritAttrs: false,
    data() {
        return {
            modalName: 'addSectionModal',
            contentSection: null,
            addSectionCfg: {
                maxItems: 1,
                create: true,
                persist: true,
                valueField: 'text',
                labelField: 'text',
                options: [
                    {text: 'Company & industry research'},
                    {text: 'Experience / education / certifications'},
                    {text: 'Projects'},
                    {text: 'Skills & interests'},
                ]
            },
        }
    },
    computed: {
        ...mapState({
            eventBus: 'eventBus',
            profile: 'profile',
            crudUrl: 'crudUrlProfile'
        }),
    },
    methods: {
        processFormData(formData) {
            if (dataUtil.isNil(formData)) {
                return null;
            }
            return {sections: JSON.stringify([...this.profile.sections, {title: formData.title, ids: []}])};
        },
        onSaveSuccess(newContentItem) {
            this.eventBus.loadContent(['profile']);
        },
    },
}
</script>
