<template>
    <BaseModal
        :modalId="modalName"
        modalTitle="Add card"
        :isLargeDisplay="true"
        @saveChange="saveChange"
    >
        <div class="btn-group mb-3" role="group">
            <input type="radio" class="btn-check" name="btnradio"
                   id="btn-existing" autocomplete="off" checked
                   @change="toggleContentType($event, contentTypes.EXISTING)"
            >
            <label class="btn btn-outline-dark" for="btn-existing">
                Existing content
                <InfoToolTip :elId="getNewElUid()" content="Existing cards and projects that you have already created."/>
            </label>

            <input type="radio" class="btn-check" name="btnradio"
                   id="btn-experience" autocomplete="off"
                   @change="toggleContentType($event, contentTypes.EXPERIENCE)"
            >
            <label class="btn btn-outline-dark" for="btn-experience">Work experience</label>

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
                Credential
                <InfoToolTip :elId="getNewElUid()" content="Add a license or certification."/>
            </label>

            <input type="radio" class="btn-check" name="btnradio"
                   id="btn-custom" autocomplete="off"
                   @change="toggleContentType($event, contentTypes.CUSTOM)"
            >
            <label class="btn btn-outline-dark" for="btn-custom">
                Custom content
                <InfoToolTip :elId="getNewElUid()" content="Add video, images, files, and descriptions to showcase anything. For example, it could be a project you created outside of the Uprove platform or research you have completed on a specific company."/>
            </label>
        </div>
        <div v-if="addContentType === contentTypes.EXISTING">
            <label class="form-label">Existing content</label>
            <ContentSelectize
                ref="contentExisting"
                :assets="initData.assets"
                @selectedContent="setContentValue"
            />
        </div>
        <EditMediaModal
            v-if="addContentType === contentTypes.CUSTOM"
            :defaultContentType="addContentType"
            :isContentOnly="true"
            ref="contentMedia"
        />
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
import EditMediaModal from "./EditMediaModal";
import InputSelectize from '../inputs/InputSelectize.vue';
import InfoToolTip from "../components/InfoToolTip";


export default {
    extends: BaseModal,
    components: {
        InfoToolTip,
        BaseModal, ContentSelectize, EditCertificationModal, EditEducationModal, EditExperienceModal, EditMediaModal, InputSelectize},
    inheritAttrs: false,
    data() {
        return {
            modalName: 'addContentModal',
            crudUrl: 'user-profile/content-item/',
            isUpdateData: true,
            mediaFields: new Set(),
            addContentType: CONTENT_TYPES.EXISTING,
            contentTypes: CONTENT_TYPES,
            isGoodContentData: null
        }
    },
    methods: {
        isGoodFormFields(formData) {
            if (this.addContentType === this.contentTypes.EXISTING && !formData.existingContentId) {
                this.addPopover($(this.$refs.contentExisting.$refs.sel.targetEl),
                    {severity: SEVERITY.WARN, content: 'You must select a piece of content to add', isOnce: true}
                );
                return false;
            }
            return this.isGoodContentData;
        },
        processFormData() {
            const mainData = this.readForm();
            let contentModal;
            if ([CONTENT_TYPES.CUSTOM, CONTENT_TYPES.VIDEO].includes(this.addContentType)) {
                contentModal = this.$refs.contentMedia;
            } else if (this.addContentType === CONTENT_TYPES.EXPERIENCE) {
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
        setContentValue({contentType, id} = {}) {
            this.formData.existingContentType = contentType;
            this.formData.existingContentId = id;
        },
        toggleContentType(e, contentType) {
            if ($(e.currentTarget).prop('checked')) {
                this.addContentType = contentType;
            } else {
                this.addContentType = null;
            }

            if (this.addContentType === this.contentTypes.CUSTOM) {
                this.eventBus.emit('open:editMediaModal:content');
            } else if (this.addContentType === this.contentTypes.EXPERIENCE) {
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
                this.$refs.contentExisting,
                this.$refs.contentMedia
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
