<template>
    <BaseModal
        :modalId="modalName"
        :modalTitle="modalTitle"
        :isLargeDisplay="true"
        @saveChange="saveChange"
    >
        <div v-if="[contentTypes.EDUCATION, contentTypes.CERTIFICATION].includes(addContentType)" class="btn-group mb-3" role="group">
            <input type="radio" class="btn-check" name="btnradio"
                   id="btn-education" autocomplete="off"
                   @change="toggleContentType($event, contentTypes.EDUCATION)"
            >
            <label class="btn btn-outline-dark" for="btn-education">Education</label>

            <input type="radio" class="btn-check" name="btnradio"
                   id="btn-certification" autocomplete="off"
                   @change="toggleContentType($event, contentTypes.CERTIFICATION)"
            >
            <label class="btn btn-outline-dark" for="btn-certification">
                Certification
                <InfoToolTip :elId="getNewElUid()" content="Add a license or certification."/>
            </label>
        </div>
        <div v-if="addContentType === contentTypes.PROJECT">
            <label class="form-label">Projects</label>
            <InputSelectize
                :elId="getNewElUid()"
                ref="contentProject"
                :isParseAsInt="true"
                :cfg="projectsCfg"
                placeholder="Select a project"
                @selected="setContentValue"
            />
        </div>
        <EditEducationModal
            v-if="addContentType === contentTypes.EDUCATION"
            ref="contentEducation"
            :isContentOnly="true"
        />
        <EditCertificationModal
            v-if="addContentType === contentTypes.CERTIFICATION"
            ref="contentCertification"
            :isContentOnly="true"
        />
        <EditExperienceModal
            v-if="addContentType === contentTypes.EXPERIENCE"
            ref="contentExperience"
            :isContentOnly="true"
        />
    </BaseModal>
</template>
<script>
import {CONTENT_TYPES, SEVERITY} from '../../globalData';
import BaseModal from './BaseModal.vue';
import ContentSelectize from '../inputs/ContentSelectize.vue';
import EditCertificationModal from "./EditCertificationModal";
import EditEducationModal from "./EditEducationModal";
import EditExperienceModal from "./EditExperienceModal";
import InputSelectize from '../inputs/InputSelectize.vue';
import InfoToolTip from "../components/InfoToolTip";
import dataUtil from "../../utils/data";


export default {
    extends: BaseModal,
    components: {
        BaseModal, ContentSelectize, EditCertificationModal, EditEducationModal, EditExperienceModal,
        InfoToolTip, InputSelectize
    },
    inheritAttrs: false,
    data() {
        return {
            modalName: 'addContentModal',
            crudUrl: 'user-profile/content-item/',
            isUpdateData: true,
            mediaFields: new Set(),
            addContentType: CONTENT_TYPES.PROJECT,
            contentTypes: CONTENT_TYPES,
            isGoodContentData: null
        }
    },
    computed: {
        modalTitle() {
            return `Add ${this.addContentType}`;
        },
        projectsCfg() {
            const options = (this.initData.assets[this.contentTypes.PROJECT] || []).map(
                (p) => ({id: p.id, title: p.customProject.projectTitle, role: p.customProject.role})
            );
            return {
                valueField: 'id',
                labelField: 'title',
                sortField: 'title',
                optgroupField: 'role',
                optgroupValueField: 'role',
                optgroupLabelField: 'role',
                options,
                optgroups: dataUtil.uniqBy(options, 'role'),
                maxItems: 1,
                closeAfterSelect: true
            }
        }
    },
    methods: {
        isGoodFormFields(formData) {
            if (this.addContentType === this.contentTypes.PROJECT && !formData.existingContentId) {
                this.addPopover($(this.$refs.contentProject.$refs.sel.targetEl),
                    {severity: SEVERITY.WARN, content: 'You must select a project', isOnce: true}
                );
                return false;
            }
            return this.isGoodContentData;
        },
        processRawData({sectionId, contentType} = {}) {
            this.addContentType = contentType;
            return {sectionId};
        },
        processFormData() {
            const mainData = this.readForm();
            let contentModal;
            if (this.addContentType === CONTENT_TYPES.EXPERIENCE) {
                contentModal = this.$refs.contentExperience;
            } else if (this.addContentType === CONTENT_TYPES.EDUCATION) {
                contentModal = this.$refs.contentEducation;
            } else if (this.addContentType === CONTENT_TYPES.CERTIFICATION) {
                contentModal = this.$refs.contentCertification;
            }

            if (contentModal) {
                const {formData: contentData, isGoodData} = contentModal.getAndCheckData();
                this.isGoodContentData = isGoodData;
                Object.assign(mainData, contentData);
                this.mediaFields = new Set([...this.mediaFields, ...(contentModal.mediaFields || [])])
            } else {
                this.isGoodContentData = true;
            }

            return Object.assign(mainData, {
                userId: this.initData.user.id,
                type: this.addContentType,
            });
        },
        setContentValue(id) {
            this.formData.existingContentType = this.contentTypes.PROJECT;
            this.formData.existingContentId = id;
        },
        toggleContentType(e, contentType) {
            if ($(e.currentTarget).prop('checked')) {
                this.addContentType = contentType;
            } else {
                this.addContentType = null;
            }

            if (this.addContentType === this.contentTypes.EXPERIENCE) {
                this.eventBus.emit('open:editExperienceModal:content');
            } else if (this.addContentType === this.contentTypes.EDUCATION) {
                this.eventBus.emit('open:editEducationModal:content');
            } else if (this.addContentType === this.contentTypes.EDUCATION) {
                this.eventBus.emit('open:editCertificationModal:content');
            }
        },
        setFormRefs() {
            this.childForms = [
                this.$refs.contentCertification,
                this.$refs.contentEducation,
                this.$refs.contentExperience,
                this.$refs.contentProject
            ]
        }
    },
    mounted() {
        this.setFormRefs();
    },
    updated() {
        this.setFormRefs();
    }
}
</script>
