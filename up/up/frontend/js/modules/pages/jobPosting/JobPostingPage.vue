<template>
    <BasePage
        :headerTitle="initData.job.jobTitle"
        :headerImage="initData.employer.logo"
        :headerImageAlt="initData.employer.companyName"
    >
        <div v-if="!initData.isAuthorized" class="row">
            <div class="col-12">
                <div class="card-custom card-custom--no-side-margin card-custom--no-top-margin -color-yellow">
                    You must sign in or <a href="#" @click="signUpWithContext">create an account</a> to see the full job details.
                </div>
            </div>
        </div>
        <div class="row mb-3 justify-content-center" :class="(isMobile) ? 'mobile-top' : ''">
            <div class="col-md-8">
                <JobPosting
                    ref="jobPosting"
                    :employer="initData.employer"
                    :job="initData.job"
                    :isJobDescriptionOpen="true"
                    :isCompanyDescriptionOpen="true"
                />
            </div>
            <div class="col-md-4 mb-3" :class="(isMobile) ? 'mobile-side-margin' : ''">
                <div class="sidebar">
                    <div v-if="!isLoggedIn">
                        To get started,
                        <a href="#" @click="signUpWithContext">create an account</a>
                        or
                        <a href="#" @click="eventBus.emit('open:signInModal')">sign in</a>
                    </div>
                    <div v-if="initData.userApplication" class="mb-2 ps-2 -color-yellow">
                        <i class="fas fa-info"></i> You have an application for this job
                    </div>
                    <div v-if="!initData.userApplication" class="-border-bottom--light pb-2 mb-2">
                        <FastApplyBtn
                            v-if="initData.job.isClient"
                            btnClasses="w-100"
                            :disabled="(isLoggedIn) ? null : true"
                            :title="(isLoggedIn) ? null : 'Must be logged in to submit application'"
                            :job="initData.job"
                        />
                        <div class="btn btn-primary w-100" @click="submitAndTrackExternalApplication">
                            Apply&nbsp;<i class="fas fa-external-link-alt"></i>
                        </div>
                    </div>
                    <div v-if="initData.job.allowedProjects.length">
                        <h6>Increase your chances of landing a job by completing a relevant project to showcase your skills</h6>
                        <ul class="fa-ul">
                            <li v-for="project in initData.job.allowedProjects">
                                <span class="fa-li">
                                    <i class="fas fa-external-link-alt"></i>
                                </span>
                                <a :href="`/project/${project.projectId}`" target="_blank">{{project.projectTitle}}</a>
                                &nbsp;<div class="badge bg-secondary rounded-pill -color-black-text">{{getUserProjectStatus(project)}}</div>
                                <div class="-text-medium" v-html="initData.projects[project.projectId].description"></div>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </BasePage>
</template>

<script>
import {getAjaxFormData, makeAjaxRequest} from "../../../vueMixins";
import AccordionItem from "../../components/AccordionItem";
import BannerAlert from "../../components/BannerAlert";
import FileDisplay from "../../components/FileDisplay";
import InfoToolTip from "../../components/InfoToolTip";
import InputSelectize from "../../inputs/InputSelectize";
import JobApplyBtn from "../jobs/JobApplyBtn";
import JobPosting from "./JobPosting";
import ListFontAwesome from "../../components/ListFontAwesome";
import PageHeader from "../../components/PageHeader";
import dataUtil from "../../../utils/data";
import BasePage from "../base/BasePage";
import FastApplyBtn from "../jobs/FastApplyBtn";

export default {
    name: "JobPostingPage.vue",
    components: {
        FastApplyBtn,
        BasePage, AccordionItem, BannerAlert, FileDisplay, InfoToolTip, InputSelectize,
        JobApplyBtn, JobPosting, ListFontAwesome, PageHeader
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
            }
        },
        hasProjectSaved() {
            return Boolean(initData?.userProjects?.length);
        }
    },
    methods: {
        isEmpty: dataUtil.isEmpty.bind(dataUtil),
        getUserProjectStatus(project) {
            if (!this.initData?.userProjects?.length) {
                return 'Not Started'
            }

            const userProject = this.initData.userProjects.find((up) => up.customProject.id === project.id);
            if (!userProject) {
                return 'Not Started';
            } else if (userProject.status === this.globalData.PROJECT_STATUSES.COMPLETE) {
                return 'Completed'
            }

            return 'In Progress';
        },
        submitAndTrackExternalApplication() {
            makeAjaxRequest(`${this.apiUrl}user-job-application/`, {
                method: 'POST',
                data: getAjaxFormData({
                    userId: this.globalData.uproveUser.id,
                    employerJobId: this.initData.job.id
                }),
                success: () => {
                    this.redirectUrl(this.initData.job.applicationUrl, true);
                },
                error: this.onSaveFailure
            });
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
        signUpWithContext() {
            dataUtil.signUpWithContext(this.initData);
        }
    },
    mounted() {
        if (this.initData.job.allowedProjects.length > 1 && !this.hasProjectSaved) {
            this.requiredFields.customProjectId = this.$refs.allowedProjects?.targetEl;
        } else if (this.initData.job.allowedProjects.length === 1) {
            this.formData.customProjectId = this.initData.job.allowedProjects[0].id;
        }
    }
}
</script>