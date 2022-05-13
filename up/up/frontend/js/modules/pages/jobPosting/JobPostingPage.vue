<template>
    <BasePage
        :headerTitle="initData.job.jobTitle"
        :headerImage="initData.employer.logo"
        :headerImageAlt="initData.employer.companyName"
    >
        <div class="row mb-3 justify-content-center" :class="(isMobile) ? 'mobile-top' : ''">
            <JobPosting
                ref="jobPosting"
                class="col-md-8"
                :employer="initData.employer"
                :job="initData.job"
                :isJobDescriptionOpen="true"
                :customProjectId="formData.customProjectId"
            />
            <div class="col-md-4 sidebar mb-3" :class="(isMobile) ? 'mobile-side-margin' : ''">
                <template v-if="initData.job?.allowedProjects?.length && initData.employer.isClient">
                    <h5 class="-text-bold">Applicant instructions</h5>
                    <div v-if="initData.userApplication" class="mb-2 ps-2 -color-yellow">
                        <i class="fas fa-info"></i> You have an application for this job
                    </div>
                    <ol class="-border-bottom--light mb-3 pb-3">
                        <li v-if="!isLoggedIn" id="loginInstruction">
                            <a href="#" @click="signUpWithContext">Create an account</a>
                            or
                            <a href="#" @click="eventBus.emit('open:signInModal')">sign in</a>
                        </li>
                        <li v-if="initData.job.allowedProjects.length > 1 && !initData.userApplication">
                            Select a project
                            <InputSelectize
                                ref="allowedProjects"
                                elId="allowedProjects"
                                placeholder="Required"
                                :isParseAsInt="true"
                                :cfg="allowedProjectsCfg"
                                @selected="selectAndSetProject"
                            />
                        </li>
                        <li>
                            Read project description, background, and instructions
                        </li>
                        <li v-if="$refs?.jobPosting?.hasFiles">
                            Download project files
                        </li>
                        <li v-if="!initData.userApplication">
                            <button
                                @click="saveChange" type="button" class="btn btn-primary w-75"
                                :disabled="(isLoggedIn) ? null : true"
                                :title="(isLoggedIn) ? null : 'Must be logged in to save project'"
                            >
                                Start project and job application
                            </button>
                        </li>
                        <li>
                            Upload your final project files and submit your final project to {{initData.employer.companyName}}
                            from your <a href="/candidateDashboard/">dashboard page</a>
                        </li>
                    </ol>
                    <div class="-sub-text">Need help or have questions about the project?</div>
                    <div class="-sub-text"><a href="#" @click="eventBus.emit('open:submitHelpModal')">Submit question</a></div>
                </template>
                <template v-else>
                    <template v-if="!isEmpty(initData.projects)">
                        <InfoToolTip
                            :elId="getNewElUid()"
                            :isExcludeInfoCircle="true"
                            content="This employer is not part of the Uprove network. You can still complete a project
                            to showcase your skills for the relevant role, however there is no guarantee the employer will
                            review it.
                            "
                        >
                            <h6>
                                <i class="fas fa-exclamation-triangle -color-orange-text"></i>
                                Projects related to this job
                            </h6>
                        </InfoToolTip>
                        <h6>Increase your chances of landing a job by completing a relevant project to showcase your skills</h6>
                        <ul class="fa-ul">
                            <li v-for="project in initData.projects">
                                <span class="fa-li">
                                    <i class="fas fa-external-link-alt"></i>
                                </span>
                                <a :href="`/project/${project.id}`" target="_blank">{{project.title}}</a>
                                <div class="-text-medium" v-html="project.description"></div>
                            </li>
                        </ul>
                    </template>
                    <div v-if="getApplicationUrl(initData.job)" class="mt-3">
                        <JobApplyBtn :applicationUrl="getApplicationUrl(initData.job)" class="w-100"/>
                    </div>
                </template>
            </div>
        </div>
    </BasePage>
    <SubmitHelpModal/>
</template>

<script>
import AccordionItem from "../../components/AccordionItem";
import BannerAlert from "../../components/BannerAlert";
import FileDisplay from "../../components/FileDisplay";
import InfoToolTip from "../../components/InfoToolTip";
import InputSelectize from "../../inputs/InputSelectize";
import JobApplyBtn from "../jobs/JobApplyBtn";
import JobPosting from "./JobPosting";
import ListFontAwesome from "../../components/ListFontAwesome";
import PageHeader from "../../components/PageHeader";
import SubmitHelpModal from "../../modals/SubmitHelpModal";
import dataUtil from "../../../utils/data";
import BasePage from "../base/BasePage";

export default {
    name: "JobPostingPage.vue",
    components: {
        BasePage, AccordionItem, BannerAlert, FileDisplay, InfoToolTip, InputSelectize,
        JobApplyBtn, JobPosting, ListFontAwesome, PageHeader, SubmitHelpModal
    },
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
            // Get projects that user has already started
            const existingCustomProjectIds = (this.initData.userProjects) ?
                this.initData.userProjects.map((up) => up.customProject.id) : [];
            return {
                maxItems: 1,
                options: this.initData.job.allowedProjects.map((ap) => {
                    return {
                        value: ap.id,
                        text: ap.projectTitle,
                        hasProject: existingCustomProjectIds.includes(ap.id)
                    }
                }),
                render: {
                    option: (data, escape) => {
                        const extraText = (data.hasProject) ? `
                            <div class="-text-small mt-2">
                                <i class="fas fa-check-circle -color-green-text"></i>
                                You have already started this project and can reuse it for this application
                            </div>
                        ` : '';

                        return `
                            <div class="option" data-selectable data-value="${data.value}" style="cursor: pointer;">
                                ${escape(data.text)}
                                ${extraText}
                            </div>
                        `;
                    }
                }
            }
        },
        hasProjectSaved() {
            return Boolean(initData?.userProjects?.length);
        }
    },
    methods: {
        isEmpty: dataUtil.isEmpty.bind(dataUtil),
        getApplicationUrl(job) {
            if (job.isClient && job.allowedProjects.length) {
                return `/job-posting/${job.id}`;
            }
            return job.applicationUrl;
        },
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
                this.formData.userProjectId = null;
                return;
            }

            // Set existing user project if it exists
            if (this.initData.userProjects) {
                const existingUserProject = this.initData.userProjects.find((up) => up.customProject.id === customProjectId);
                if (existingUserProject) {
                    this.formData.userProjectId = existingUserProject.id;
                }
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
        if (this.initData.job.allowedProjects.length > 1 && !this.hasProjectSaved) {
            this.requiredFields.customProjectId = this.$refs.allowedProjects.targetEl;
        } else if (this.initData.job.allowedProjects.length === 1) {
            this.formData.customProjectId = this.initData.job.allowedProjects[0].id;
        }
    }
}
</script>