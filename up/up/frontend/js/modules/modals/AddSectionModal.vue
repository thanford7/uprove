<template>
    <BaseModal
        :modalId="modalName"
        modalTitle="Add section"
        :isLargeDisplay="true"
        @saveChange="saveChange"
    >
        <div class="mb-3">
            <label class="form-label">Section title</label>
            <InputSelectize
                ref="selTitle"
                :elId="getNewElUid()"
                :cfg="addSectionCfg"
                placeholder="Add or select a new section title"
                @selected="formData.title = $event"
            />
        </div>
    </BaseModal>
</template>
<script>
import BaseModal from './BaseModal.vue';
import InputSelectize from '../inputs/InputSelectize.vue';

export default {
    extends: BaseModal,
    components: {BaseModal, InputSelectize},
    inheritAttrs: false,
    data() {
        return {
            modalName: 'addSectionModal',
            crudUrl: 'user-profile/section/',
            isUpdateData: true,
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
            requiredFields: {
                title: null
            }
        }
    },
    methods: {
        processRawData(rawData) {
            this.requiredFields.title = this.$refs.selTitle.targetEl
            return rawData;
        },
        processFormData() {
            const data = this.readForm();
            data.profileId = this.initData.id;
            return data;
        }
    }
}
</script>
