<template>
    <BasePage>
        <div class="row mt-4" :class="(isMobile) ? 'mobile-top' : ''">
            <ProjectAccordion
                class="mt-3"
                :class="(isCandidate) ? 'col' : 'col-md-8'"
                :project="initData.project"
                :skills="initData.skills"
                :skillIds="formData.skillIds"
            >
                <template v-if="isCandidate" v-slot:headerAppend>
                    <button
                        v-if="!initData.userProject"
                        id="candidateSaveButton"
                        @click="readAndSubmitForm"
                        type="button" class="btn btn-primary" style="float: right;"
                    >Save project to dashboard</button>
                </template>
                <template v-slot:afterHeader>
                    <div v-if="initData.userProject" class="mb-2 ps-2 -color-yellow">
                        <i class="fas fa-info"></i> You have already started this project
                    </div>
                </template>
            </ProjectAccordion>
            <div v-if="initData.project.isLimited" class="col-md-3 sidebar mb-3" :class="(isMobile) ? 'mobile-side-margin' : ''">
                <div class="-text-center">
                    Want to view the full project brief and files?
                </div>
                <div>
                    <button type="button" class="btn btn-sm btn-primary w-100" @click="redirectUrl('/sign-up/')">
                        Get started
                    </button>
                </div>
            </div>
            <div
                v-if="isEmployer && initData?.jobs?.length"
                class="col-md-3 sidebar mb-3" :class="(isMobile) ? 'mobile-side-margin' : ''"
            >
                <h5>
                    Current jobs
                    <InfoToolTip :elId="getNewElUid()" content="Job openings that are linked to this project. This means that any candidate who has completed this project can apply to any of these job openings."/>
                </h5>
                <ListFontAwesome faClassesStr="fas fa-briefcase" :items="initData.jobs.map((j) => getUniqueJobTitle(j))"/>
            </div>
        </div>
    </BasePage>
    <EditUserModal/>
    <EmployerRequestInfoModal/>
</template>

<script>
import BasePage from "../base/BasePage";
import EditUserModal from "../../modals/EditUserModal";
import EmployerRequestInfoModal from "../../modals/EmployerRequestInfoModal";
import InfoToolTip from "../../components/InfoToolTip";
import ListFontAwesome from "../../components/ListFontAwesome";
import skillLevelSelectize from "../../selectizeCfgs/skillLevels";
import SkillsSelectize from "../../inputs/SkillsSelectize";
import ProjectAccordion from "./ProjectAccordion";

export default {
    name: "ProjectPage.vue",
    components: {
        BasePage, EditUserModal, EmployerRequestInfoModal, InfoToolTip, ListFontAwesome, ProjectAccordion, SkillsSelectize
    },
    data() {
        return {
            crudUrl: 'user-project/',
            pageRedirect: null, // Set on mounted
            isUpdateData: true,
            initDataKey: 'userProjects',
        }
    },
    methods: {
        getSuccessMessage() {
            return 'Added project to profile';
        },
        getFailureMessagePrepend() {
            return 'Failed to add project: ';
        },
        getUniqueJobTitle(job) {
            let title = job.jobTitle;
            if (job.city || job.state) {
                title += ` (${' ,'.join([job.city, job.state])})`
            }
            return title;
        },
        processFormData() {
            const formData = this.readForm();
            formData.userId = this.globalData.uproveUser.id;
            formData.projectId = this.initData.project.id;
            return formData;
        },
        setJobSkillLevels(jobs) {
            jobs.forEach((j) => { skillLevelSelectize.setSkillLevels(j.allowedProjects,  true); });
        },
    },
    mounted() {
        // Set skill levels from bits
        if (this.initData.jobs) {
            this.setJobSkillLevels(this.initData.jobs);
        }

        if (this.isCandidate) {
            this.pageRedirect = `/candidateDashboard/${this.globalData.uproveUser.id}/`;
        }
    }
}
</script>