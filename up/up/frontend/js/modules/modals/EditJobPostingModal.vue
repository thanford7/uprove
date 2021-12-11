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
            <label for="modalJobProjects" class="form-label">Applicant Project(s)</label>
            <InputSelectize
                ref="jobProjects"
                elId="modalJobProjects"
                :isParseAsInts="true"
                placeholder="Required" :cfg="projectsCfg" @selected="formData.projectIds = $event"
            />
        </div>
    </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal";
import InputSelectize from "../inputs/InputSelectize";
import InputWsiwyg from "../inputs/InputWsiwyg";

export default {
    name: "EditJobPostingModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal, InputSelectize, InputWsiwyg},
    data() {
        return {
            modalName: 'editJobPostingModal',
            crudUrl: 'job-posting/',
            isUpdateData: true,
            initDataKey: 'employer.jobs',
            requiredFields: {
                jobTitle: 'modal-jobTitle',
                jobDescription: 'modal-jobDescription'
            },
        }
    },
    computed: {
        projectsCfg() {
            return {
                plugins: ['uprove', 'remove_button'],
                maxItems: null,
                optgroups: _.sortBy(_.uniqBy(this.initData.projects.map((p) => ({group: p.function})), 'group'), ['group']),
                optgroupValueField: 'group',
                optgroupLabelField: 'group',
                optgroupField: 'function',
                valueField: 'id',
                labelField: 'title',
                searchField: ['title', 'function'],
                options: this.initData.projects,
                render: {
                    option: (data, escape) => {
                        let skillsHtml = '';
                        data.skills.forEach((skill) => {
                            skillsHtml += `<div class="badge -color-lightblue -color-black-text me-1">${escape(skill.name)}</div>`
                        })
                        const getProjectUrl = (projectId) => `/project/${projectId}/`;
                        return `
                            <div class="option">
                                <div class="mb-1">
                                    ${escape(data.title)}
                                    <a href="${getProjectUrl(data.id)}" title="Open full project description"><i class="fas fa-external-link-alt"></i></a>
                                </div>
                                <div class="-sub-text">${data.description}</div>
                                <div><span class="-sub-text">Skills: </span>${skillsHtml}</div>
                            </div>
                        `;
                    }
                }
            };
        }
    }
}
</script>