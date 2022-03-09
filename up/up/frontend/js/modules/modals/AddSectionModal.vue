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
import {SEVERITY} from '../../globalData';
import BaseModal from './BaseModal.vue';
import InputSelectize from '../inputs/InputSelectize.vue';

export default {
    extends: BaseModal,
    components: {BaseModal, InputSelectize},
    inheritAttrs: false,
    computed: {
        currentSections() {
            return this.initData.sections.map((s) => s.title.toLowerCase());
        },
        addSectionCfg() {
            const defaultOptions = [
                {text: 'Company & industry research'},
                {text: 'Experience / education / certifications'},
                {text: 'Projects'},
                {text: 'Skills & interests'},
            ]

            return {
                maxItems: 1,
                create: true,
                persist: true,
                valueField: 'text',
                labelField: 'text',
                options: defaultOptions.filter((opt) => !this.isCurrentSection(opt.text))
            }
        },
    },
    data() {
        return {
            modalName: 'addSectionModal',
            crudUrl: 'user-profile/section/',
            isUpdateData: true,
            contentSection: null,
            requiredFields: {
                title: null
            }
        }
    },
    methods: {
        isCurrentSection(sectionTitle) {
            return this.currentSections.includes(sectionTitle.toLowerCase());
        },
        processFormData() {
            const data = this.readForm();
            data.profileId = this.initData.id;
            return data;
        },
        isGoodFormFields(formData) {
            if(this.isCurrentSection(formData.title)) {
                this.addPopover($(this.$refs.selTitle.targetEl),
                {severity: SEVERITY.WARN, content: 'You have already added a section with this name.', isOnce: true}
                    );
                return false;
            }
            return true;
        },
    },
    mounted() {
        this.requiredFields.title = this.$refs.selTitle.targetEl;
    }
}
</script>
