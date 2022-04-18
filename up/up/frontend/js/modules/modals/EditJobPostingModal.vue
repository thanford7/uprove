<template>
    <BaseModal
        :modalId="modalName"
        :modalTitle="(formData.id) ? `Edit posting: ${formData.jobTitle}`: 'Create new posting'"
        :primaryButtonText="(formData.id) ? 'Save changes' : 'Create posting'"
        :isLargeDisplay="true"
        :isScrollable="true"
        :isAllowDelete="Boolean(formData.id)"
        @saveChange="saveChange($event)"
        @deleteObject="deleteObject($event)"
    >
        <div class="mb-3">
            <label for="modalJobTitle" class="form-label">Job Title</label>
            <input type="text" class="form-control" placeholder="Required" id="modalJobTitle" v-model="formData.jobTitle">
        </div>
        <div class="mb-3">
            <label for="modalJobDescription" class="form-label">Job Description</label>
            <InputWsiwyg
                ref="jobDescription"
                elId="modalJobDescription"
                placeholder="Add a description..."
                v-model="formData.jobDescription"
            />
            <div class="row align-items-center">
                <div class="col-5 pe-0">
                    <InputSelectize
                        ref="jobTemplate"
                        elId="modalJobTemplate"
                        :isParseAsInt="true"
                        placeholder="Start from template" :cfg="templateCfg" @selected="updateJobDescription"
                    />
                </div>
                <div class="col-1 ps-1">
                    <InfoToolTip :elId="getNewElUid()" :content="infoJobTemplate"/>
                </div>
            </div>
        </div>
        <div class="mb-3">
            <label for="openDate" class="form-label">Open Date <InfoToolTip :content="TOOLTIPS.jobStartDate" :elId="getNewElUid()"/></label>
            <input type="date" class="form-control" id="openDate" v-model="formData.openDate">
            <span class="-sub-text">Leave blank for "DRAFT" status</span>
        </div>
        <div v-if="formData.id" class="mb-3">
            <label for="pauseDate" class="form-label">Pause Date <InfoToolTip :content="TOOLTIPS.jobPauseDate" :elId="getNewElUid()"/></label>
            <input type="date" class="form-control" id="pauseDate" v-model="formData.pauseDate">
        </div>
        <div v-if="formData.id" class="mb-3">
            <label for="closeDate" class="form-label">Close Date <InfoToolTip :content="TOOLTIPS.jobCloseDate" :elId="getNewElUid()"/></label>
            <input type="date" class="form-control" id="closeDate" v-model="formData.closeDate">
        </div>
        <div class="mb-3">
            <label for="modalJobProjects" class="form-label">
                Applicant Project(s) <InfoToolTip :content="infoApplicantProject" :elId="getNewElUid()"/>
            </label>
            <ProjectsSelectize
                ref="jobProjects"
                :isAllowMulti="true"
                :employerId="initData.employer.id"
                :allowedProjects="formData.allowedProjects"
                @projectChange="formData.allowedProjects = $event"
            />
        </div>
        <div class="mb-3 pt-1 border-top" v-for="customProject in formData.allowedProjects">
            <ProjectConfigSelectize
                :employerId="initData.employer.id"
                :customProject="customProject"
                :project="getProject(customProject.projectId)"
            />
        </div>
    </BaseModal>
</template>

<script>
import {SEVERITY} from '../../globalData';
import BaseModal from "./BaseModal";
import dataUtil from "../../utils/data";
import form from "../../utils/form";
import InfoToolTip from "../components/InfoToolTip";
import InputSelectize from "../inputs/InputSelectize";
import InputWsiwyg from "../inputs/InputWsiwyg";
import ProjectConfigSelectize from "../inputs/ProjectConfigSelectize";
import ProjectsSelectize from "../inputs/ProjectsSelectize";
import $ from "jquery";

export default {
    name: "EditJobPostingModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    components: {ProjectsSelectize, ProjectConfigSelectize, BaseModal, InfoToolTip, InputSelectize, InputWsiwyg},
    data() {
        return {
            modalName: 'editJobPostingModal',
            crudUrl: 'job-posting/',
            isUpdateData: true,
            initDataKey: 'employer.jobs',
            requiredFields: {
                jobTitle: '#modalJobTitle',
                jobDescription: '#modalJobDescription',
            },
            infoApplicantProject: (
                'Select one or more projects which applicants to this job position will need to complete. ' +
                'If more than one project is selected, each applicant will only need to complete one project, but ' +
                'will be able to select which project to complete.'
            ),
            infoJobTemplate: (
                'Selecting a job template will add suggested language for a job description to the job description ' +
                'section above. If a description already exists, it will NOT be erased. The suggested language will ' +
                'be added to the end of the text.'
            )
        }
    },
    computed: {
        templateCfg() {
            return {
                maxItems: 1,
                sortField: 'text',
                options: this.initData.jobTemplates.map((e) => ({value: e.id, text: e.title}))
            }
        },
    },
    methods: {
        getProject(projectId) {
            return this.initData.projects.find((project) => project.id === projectId);
        },
        processFormData() {
            return Object.assign(this.readForm(), {employerId: this.initData.employer.id})
        },
        setFormFields() {
            this.formData.allowedProjects.forEach((ap) => {
                // Format data for ajax request
                ap.skillIds = ap.skills.map((s) => s.id);
            });

        },
        getEmptyFormData() {
            return {
                allowedProjects: []
            }
        },
        isGoodFormFields(formData) {
            if (form.isEmptyWysiwyg(formData.jobDescription)) {
                this.addPopover($('#modalJobDescription'),
                {severity: SEVERITY.WARN, content: 'Required field', isOnce: true}
                    );
                return false;
            }

            if (!formData.allowedProjects || !formData.allowedProjects.length) {
                this.addPopover($(this.$refs.jobProjects.$refs.projects.targetEl),
                {severity: SEVERITY.WARN, content: 'Required field', isOnce: true}
                    );
                return false;
            }

            for (let i = 0; i < formData.allowedProjects.length; i++) {
                const customProject = formData.allowedProjects[i];
                if (dataUtil.isNil(customProject.skillLevelBit)) {
                    this.addPopover($(this.$refs[`modalJobCustomProject-skillBits-${customProject.id}`].targetEl),
                    {severity: SEVERITY.WARN, content: 'Required field', isOnce: true}
                        );
                    return false;
                }

                if (dataUtil.isNil(customProject.skillIds)) {
                    this.addPopover($(this.$refs[`modalJobCustomProject-skills-${customProject.id}`].targetEl),
                    {severity: SEVERITY.WARN, content: 'Required field', isOnce: true}
                        );
                    return false;
                }
            }

            return true;
        },
        updateJobDescription(templateId) {
            if (!templateId) {
                return;
            }
            const template = this.initData.jobTemplates.find((jt) => jt.id === templateId);
            this.$refs.jobDescription.addContent(template.description);
        }
    },

}
</script>