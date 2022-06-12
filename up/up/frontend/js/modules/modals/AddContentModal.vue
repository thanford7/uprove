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
                   checked
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
            <label class="form-label">
                Projects&nbsp;<InfoToolTip :elId="getNewElUid()" content="Only projects that are completed and not hidden can be added to your profile. You can change these project settings on your dashboard page."/>
            </label>
            <InputSelectize
                :elId="getNewElUid()"
                ref="contentProject"
                :isParseAsInt="true"
                :cfg="projectsCfg"
                :placeholder="(projectOptions.length) ? 'Select a project' : 'No projects available to select'"
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
import PROJECT_STATUSES, {CONTENT_TYPES, PROFILE_SECTIONS, SEVERITY} from '../../globalData';
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
        projectOptions() {
            const alreadySelectedIds = this.initData.sections
                .find((s) => s.sectionType === PROFILE_SECTIONS.PROJECTS)
                .sectionItems.map((si) => si.item.id)
            return (this.initData.assets[this.contentTypes.PROJECT] || [])
                .filter((p) => !alreadySelectedIds.includes(p.id) && !p.isHidden && p.status === this.globalData.PROJECT_STATUSES.COMPLETE)
                .map((p) => ({id: p.id, title: p.customProject.projectTitle, role: p.customProject.role})
            );
        },
        projectsCfg() {
            return {
                valueField: 'id',
                labelField: 'title',
                sortField: 'title',
                optgroupField: 'role',
                optgroupValueField: 'role',
                optgroupLabelField: 'role',
                options: this.projectOptions,
                optgroups: dataUtil.uniqBy(this.projectOptions, 'role'),
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

            if (this.$refs.contentProject && !this.projectOptions.length) {
                this.$refs.contentProject.elSel.disable();
            }
        }
    },
    mounted() {
        this.setFormRefs();
        this.eventBus.on('formClear', () => {
            const educationToggleButton$ = $('#btn-education');
            if(educationToggleButton$.length) {
                educationToggleButton$.click();
            }
        })
    },
    updated() {
        this.setFormRefs();
    }
}
</script>
