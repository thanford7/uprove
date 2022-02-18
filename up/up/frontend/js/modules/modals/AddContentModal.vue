<template>
    <BaseModal
        :modalId="modalName"
        modalTitle="Add content"
        :isLargeDisplay="true"
        @saveChange="saveChange"
    >
        <div class="btn-group mb-3" role="group">
            <input type="radio" class="btn-check" name="btnradio"
                   id="btn-existing" autocomplete="off" checked
                   @change="toggleContentType($event, contentTypes.EXISTING)"
            >
            <label class="btn btn-outline-dark" for="btn-existing">Existing content</label>

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
                   id="btn-custom" autocomplete="off"
                   @change="toggleContentType($event, contentTypes.CUSTOM)"
            >
            <label class="btn btn-outline-dark" for="btn-custom">Custom project</label>

            <input type="radio" class="btn-check" name="btnradio"
                   id="btn-video" autocomplete="off"
                   @change="toggleContentType($event, contentTypes.VIDEO)"
            >
            <label class="btn btn-outline-dark" for="btn-video">Video</label>
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
            v-if="[contentTypes.VIDEO, contentTypes.CUSTOM].includes(addContentType)"
            :defaultContentType="addContentType"
            :isContentOnly="true"
            ref="contentMedia"
        />
        <EditEducationModal
            v-if="addContentType === contentTypes.EDUCATION"
            ref="contentEducation"
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
import {CONTENT_TYPES} from '../../globalData';
import {severity} from "../../vueMixins";
import BaseModal from './BaseModal.vue';
import ContentSelectize from '../inputs/ContentSelectize.vue';
import EditEducationModal from "./EditEducationModal";
import EditExperienceModal from "./EditExperienceModal";
import EditMediaModal from "./EditMediaModal";
import InputSelectize from '../inputs/InputSelectize.vue';


export default {
    extends: BaseModal,
    components: {BaseModal, ContentSelectize, EditEducationModal, EditExperienceModal, EditMediaModal, InputSelectize},
    inheritAttrs: false,
    data() {
        return {
            modalName: 'addContentModal',
            crudUrl: 'user-profile/content-item/',
            isUpdateData: true,
            mediaFields: [],
            addContentType: CONTENT_TYPES.EXISTING,
            contentTypes: CONTENT_TYPES,
            isGoodContentData: null
        }
    },
    methods: {
        isGoodFormFields(formData) {
            if (this.addContentType === this.contentTypes.EXISTING && !formData.existingContentId) {
                this.addPopover($(this.$refs.contentExisting.$refs.sel.targetEl),
                    {severity: severity.WARN, content: 'You must select a piece of content to add', isOnce: true}
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
                contentModal = this.$refs.contentEducation
            }

            if (contentModal) {
                const {formData: contentData, isGoodData} = contentModal.getAndCheckData();
                this.isGoodContentData = isGoodData;
                Object.assign(mainData, contentData);
                this.mediaFields = [...this.mediaFields, ...(contentModal.mediaFields || [])]
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

            if ([this.contentTypes.VIDEO, this.contentTypes.CUSTOM].includes(this.addContentType)) {
                this.eventBus.emit('open:editMediaModal:content');
            }
            if (this.addContentType === this.contentTypes.EXPERIENCE) {
                this.eventBus.emit('open:editExperienceModal:content');
            }
            if (this.addContentType === this.contentTypes.EDUCATION) {
                this.eventBus.emit('open:editEducationModal:content');
            }
        }
    }
}
</script>
