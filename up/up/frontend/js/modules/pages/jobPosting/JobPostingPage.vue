<template>
    <BasePage
        :headerTitle="initData.job.jobTitle"
        :headerImage="initData.employer.logo"
        :headerImageAlt="initData.employer.companyName"
    >
        <div class="row mb-3 justify-content-center" :class="(isMobile) ? 'mobile-top' : ''">
            <JobPosting
                ref="jobPosting"
                class="col-md-9"
                :employer="initData.employer"
                :job="initData.job"
                :customProjectId="formData.customProjectId"
            />
            <div class="col-md-3 sidebar mb-3" :class="(isMobile) ? 'mobile-side-margin' : ''">
                <h5 class="-text-bold">Applicant instructions</h5>
                <ol class="-border-bottom--light mb-3 pb-3">
                    <li v-if="!isLoggedIn" id="loginInstruction">
                        <a href="#" @click="signUpWithContext">Create an account</a>
                        or
                        <a href="#" @click="eventBus.emit('open:signInModal')">sign in</a>
                    </li>
                    <li v-if="initData.job.allowedProjects.length > 1 && !hasProjectSaved">
                        Select a project
                        <InputSelectize
                            ref="allowedProjects"
                            elId="allowedProjects"
                            placeholder="Required" :cfg="allowedProjectsCfg" @selected="selectAndSetProject"
                        />
                    </li>
                    <li>
                        Read project description, background, and instructions
                    </li>
                    <li v-if="$refs?.jobPosting?.hasFiles">
                        Download project files
                    </li>
                    <li v-if="!hasProjectSaved">
                        <button
                            @click="saveChange" type="button" class="btn btn-primary w-75"
                            :disabled="(isLoggedIn) ? null : true"
                            :title="(isLoggedIn) ? null : 'Must be logged in to save project'"
                        >
                            Save project to your profile
                        </button>
                    </li>
                    <li>
                        Upload your final project files and submit your final project to {{initData.employer.companyName}}
                        from your home page
                    </li>
                </ol>
                <div class="-sub-text">Need help or have questions about the project?</div>
                <div class="-sub-text"><a href="#" @click="eventBus.emit('open:submitHelpModal')">Submit question</a></div>
            </div>
        </div>
    </BasePage>
    <SubmitHelpModal/>
</template>

<script>
import AccordionItem from "../../components/AccordionItem";
import BannerAlert from "../../components/BannerAlert";
import FileDisplay from "../../components/FileDisplay";
import InputSelectize from "../../inputs/InputSelectize";
import JobPosting from "./JobPosting";
import PageHeader from "../../components/PageHeader";
import SubmitHelpModal from "../../modals/SubmitHelpModal";
import dataUtil from "../../../utils/data";
import BasePage from "../base/BasePage";

export default {
    name: "JobPostingPage.vue",
    components: {BasePage, AccordionItem, BannerAlert, FileDisplay, InputSelectize, JobPosting, PageHeader, SubmitHelpModal},
    data() {
        return {
            accordionElId: `accordion-${this.getNewElUid()}`,
            crudUrl: 'user-job-application/',
            requiredFields: {
                customProjectId: null,
                userId: '#loginInstruction'
            },
            pageRedirect: '/candidateDashboard/'
        }
    },
    computed: {
        allowedProjectsCfg() {
            return {
                maxItems: 1,
                options: this.initData.job.allowedProjects.map((ap) => ({value: ap.id, text: ap.projectTitle}))
            }
        },
        hasProjectSaved() {
            return initData.userProjects && initData.userProjects.length;
        }
    },
    methods: {
        processFormData() {
            return Object.assign(this.readForm(), {
                'userId': this.globalData.uproveUser.id,
                'employerJobId': this.initData.job.id
            })
        },
        getAjaxCfgOverride() {
            return {method: 'POST'}
        },
        selectAndSetProject(customProjectId) {
            this.formData.customProjectId = customProjectId;
            if (!customProjectId) {
                return;
            }
            const accordionItem = this.$refs.jobPosting.$refs[`accordionItem-${customProjectId}`];
            $(`#${accordionItem.accordionElId}`).find('.accordion-header').each((idx, el) => {
                const isShown = $(el).prop('id') === accordionItem.headerElId;
                const accordionButton = $(el).find('button.accordion-button');
                if (isShown === accordionButton.hasClass('collapsed')) {
                    accordionButton.click();
                }
            });
        },
        signUpWithContext() {
            dataUtil.signUpWithContext(this.initData);
        }
    },
    mounted() {
        if (this.initData.job.allowedProjects.length > 1) {
            this.requiredFields.customProjectId = this.$refs.allowedProjects.targetEl;
        } else if (this.initData.job.allowedProjects.length) {
            this.formData.customProjectId = this.initData.job.allowedProjects[0].id;
        }
    }
}
</script>