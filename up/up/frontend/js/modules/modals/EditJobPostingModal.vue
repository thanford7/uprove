<template>
    <BaseModal
        :modalId="modalName"
        :modalTitle="(formData.id) ? `Edit posting: ${formData.jobTitle}`: 'Create new posting'"
        :primaryButtonText="(formData.id) ? 'Save changes' : 'Create posting'"
        :isLargeDisplay="true"
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
                elId="modalJobDescription"
                placeholder="Add a description..."
                v-model="formData.jobDescription"
            />
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
            <label for="modalJobProjects" class="form-label">Applicant Project(s)</label>
            <InputSelectize
                ref="jobProjects"
                elId="modalJobProjects"
                :isParseAsInt="true"
                placeholder="Required" :cfg="projectsCfg" @selected="updateCustomProjects"
            />
        </div>
        <div class="mb-3 pt-1 border-top" v-for="customProject in formData.allowedProjects">
            <label :for="`modalJobCustomProject-skillBits-${customProject.id}`" class="form-label">
                Customize {{getProject(customProject.projectId).title}} Project
                <a href="#" @click="openCustomProject(customProject)"><i class="fas fa-external-link-alt"></i> View customized project</a>
            </label>
            <InputSelectize
                :ref="`modalJobCustomProject-skillBits-${customProject.id}`"
                :elId="`modalJobCustomProject-skillBits-${customProject.id}`"
                :items="[customProject.skillLevelBit]"
                :isParseAsBits="true"
                placeholder="Skill level (required)"
                :cfg="getProjectSkillLevelsCfg(customProject)"
                @selected="customProject.skillLevelBit = $event"
            />
            <InputSelectize
                :ref="`modalJobCustomProject-skills-${customProject.id}`"
                :elId="`modalJobCustomProject-skills-${customProject.id}`"
                :items="customProject.skillIds"
                :isParseAsInt="true"
                placeholder="Skills (required)" :cfg="getProjectSkillsCfg(customProject)" @selected="customProject.skillIds = $event"
            />
        </div>
    </BaseModal>
</template>

<script>
import {severity} from "../../vueMixins";
import BaseModal from "./BaseModal";
import dataUtil from "../../utils/data";
import InfoToolTip from "../components/InfoToolTip";
import InputSelectize from "../inputs/InputSelectize";
import InputWsiwyg from "../inputs/InputWsiwyg";
import form from "../../utils/form";
import $ from "jquery";

export default {
    name: "EditJobPostingModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal, InfoToolTip, InputSelectize, InputWsiwyg},
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
            newProjectCount: 0
        }
    },
    computed: {
        projectsCfg() {
            return {
                plugins: ['uprove', 'remove_button'],
                maxItems: null,
                optgroups: dataUtil.sortBy(dataUtil.uniqBy(this.initData.projects.map((p) => ({group: p.function})), 'group'), 'group'),
                optgroupValueField: 'group',
                optgroupLabelField: 'group',
                optgroupField: 'function',
                valueField: 'id',
                labelField: 'title',
                searchField: ['title', 'function'],
                options: this.initData.projects,
                closeAfterSelect: true,
                render: {
                    option: (data, escape) => {
                        let skillsHtml = '';
                        data.skills.forEach((skill) => {
                            skillsHtml += `<div class="badge -color-lightblue -color-black-text me-1">${escape(skill.skillName)}</div>`
                        });
                        let skillLevelsHtml = '';
                        dataUtil.getSkillLevelsFromBits(data.skillLevelBits, this.globalData.SKILL_LEVEL).forEach((skillLevel) => {
                            skillLevelsHtml += `<div class="badge -color-lightgrey -color-black-text me-1">${escape(skillLevel)}</div>`
                        });
                        const getProjectUrl = (projectId) => `/project/${projectId}/`;
                        return `
                            <div class="option" data-selectable data-value="${data.id}">
                                <div class="mb-1">
                                    ${escape(data.title)}
                                    <a href="${getProjectUrl(data.id)}" title="Open full project description"><i class="fas fa-external-link-alt"></i></a>
                                </div>
                                <div class="-sub-text">${data.description}</div>
                                <div><span class="-sub-text">Skills: </span>${skillsHtml}</div>
                                <div class="mt-1"><span class="-sub-text">Role levels: </span>${skillLevelsHtml}</div>
                            </div>
                        `;
                    }
                }
            };
        }
    },
    methods: {
        setCustomProjectSkillLevel(customProject) {
            const project = this.getProject(customProject.projectId);
            const skillLevels = this.getSkillLevelNumbersFromBits(project.skillLevelBits);
            customProject.skillLevelBit = customProject.skillLevelBit || (skillLevels && skillLevels.length === 1) ? skillLevels : null;
            return customProject.skillLevelBit;
        },
        getSkillLevelNumbersFromBits(skillLevelBits) {
            return dataUtil.getSkillLevelNumbersFromBits(skillLevelBits, this.globalData.SKILL_LEVEL);
        },
        getProject(projectId) {
            return this.initData.projects.find((project) => project.id === projectId);
        },
        getProjectSkillLevelsCfg(customProject) {
            const project = this.getProject(customProject.projectId);
            const skillLevels = this.getSkillLevelNumbersFromBits(project.skillLevelBits);
            return {
                maxItems: 1,
                options: Object
                    .entries(this.globalData.SKILL_LEVEL)
                    .filter(([key, txt]) => skillLevels.includes(key))
                    .map(([key, txt]) => ({value: key, text: txt}))
            }
        },
        getProjectSkillsCfg(customProject) {
            const project = this.getProject(customProject.projectId);
            return {
                plugins: ['remove_button'],
                maxItems: null,
                options: dataUtil.sortBy(project.skills.map((s) => ({value: s.id, text: s.skillName})), 'text')
            };
        },
        openCustomProject(customProject) {
            const skillHref = (customProject.skillIds || []).reduce((skillHref, sId) => {
                skillHref += `&skill=${sId}`;
                return skillHref;
            }, '');
            const href = `/project/${customProject.projectId}/?skillLevel=${customProject.skillLevelBit}${skillHref}`;
            window.open(href, '_blank').focus();
        },
        processFormData() {
            return Object.assign(this.readForm(), {employerId: this.initData.employer.id})
        },
        setFormFields() {
            this.$refs.jobProjects.elSel.setValue(this.formData.allowedProjects.map((ap) => ap.projectId));
            this.formData.allowedProjects.forEach((ap) => {
                ap.skillIds = ap.skills.map((s) => s.id);
            })
        },
        setEmptyFormData() {
            this.formData = {
                allowedProjects: []
            }
        },
        isGoodFormFields(formData) {
            if (form.isEmptyWysiwyg(formData.jobDescription)) {
                this.addPopover($('#modal-jobDescription'),
                {severity: severity.WARN, content: 'Required field', isOnce: true}
                    );
                return false;
            }

            if (!formData.allowedProjects || !formData.allowedProjects.length) {
                this.addPopover($(this.$refs['jobProjects'].targetEl),
                {severity: severity.WARN, content: 'Required field', isOnce: true}
                    );
                return false;
            }

            for (let i = 0; i < formData.allowedProjects.length; i++) {
                const customProject = formData.allowedProjects[i];
                if (dataUtil.isNil(customProject.skillLevelBit)) {
                    this.addPopover($(this.$refs[`modalJobCustomProject-skillBits-${customProject.id}`].targetEl),
                    {severity: severity.WARN, content: 'Required field', isOnce: true}
                        );
                    return false;
                }

                if (dataUtil.isNil(customProject.skillIds)) {
                    this.addPopover($(this.$refs[`modalJobCustomProject-skills-${customProject.id}`].targetEl),
                    {severity: severity.WARN, content: 'Required field', isOnce: true}
                        );
                    return false;
                }
            }

            return true;
        },
        updateCustomProjects(projectIds) {
            // Remove projects that are no longer selected
            this.formData.allowedProjects = this.formData.allowedProjects.filter((ap) => projectIds.includes(ap.projectId));

            // Add new projects
            const currentProjectIds = this.formData.allowedProjects.map((ap) => ap.projectId);
            projectIds.forEach((projectId) => {
                if (!currentProjectIds.includes(projectId)) {
                    this.formData.allowedProjects.push({
                        id: `new-${this.newProjectCount}`,
                        projectId
                    })
                    this.newProjectCount++;
                }
            });
        }
    }
}
</script>