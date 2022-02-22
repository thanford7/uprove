<template>
    <div class="container-lg">
        <BannerAlert/>
        <PageHeader title="Dashboard" :image="initData.user.profileImage"/>
        <div class="row mb-3 justify-content-center">
            <div class="col-md-9 card-custom table-responsive-md">
                <h3 style="display: inline-block">Projects</h3>
                <div class="row justify-content-center mt-2">
                    <BaseCard
                        v-for="userProject in initData.userProjects"
                        :cardItem="userProject"
                        :elId="getNewElUid()"
                        :isShowViewMoreLink="false"
                        class="badge-card-top"
                    >
                        <template v-slot:topImage>
                            <div class="badge badge-top -color-darkblue">{{userProject.customProject.role}}</div>
                        </template>
                        <template v-slot:header>
                            {{userProject.customProject.projectTitle}}
                        </template>
                        <template v-slot:body>
                            <div class="mb-1 pb-1 -border-bottom--light">
                                <div class="text-label text-label-sm">CAREER LEVELS</div>
                                <BadgesSkillLevels :skillLevels="userProject.customProject.skillLevels"/>
                            </div>
                            <div class="mb-1 pb-1 -border-bottom--light">
                                <div class="text-label text-label-sm">SKILLS</div>
                                <BadgesSkills :skills="userProject.customProject.skills"/>
                            </div>
                            <div>
                                <a href="#" @click="eventBus.emit('open:editUserProjectModal', userProject)">
                                    Edit project
                                </a>
                            </div>
                            <div>
                                <a :href="`/project/${userProject.customProject.projectId}/?${getCustomProjectQueryParams(userProject.customProject)}`" target="_blank">
                                    <i class="fas fa-external-link-alt"></i>
                                    View project instructions
                                </a>
                            </div>
                            <div class="dropdown mt-2 mb-2">
                                <button class="btn btn-secondary btn-sm dropdown-toggle w-100" type="button" id="projectStatus"
                                        data-bs-toggle="dropdown" aria-expanded="false" :disabled="(userProject.isLocked) ? true : null"
                                        :title="(userProject.isLocked) ? `Project cannot be changed for another ${pluralize('day', userProject.daysUntilUnlock)} to give employers time to review` : null"
                                >
                                    <i v-if="userProject.isLocked" class="fas fa-lock"></i>
                                    Project status: {{capitalize(userProject.status)}}
                                </button>
                                <ul class="dropdown-menu" aria-labelledby="projectStatus">
                                    <li>
                                        <a class="dropdown-item" href="#" @click="setProjectStatus(userProject, projectStatuses.DRAFT)">
                                            <InfoToolTip :elId="getNewElUid()" :isHtmlContent="true" :content="CONTENT.draftStatusInfo"/>
                                            Draft
                                        </a>
                                    </li>
                                    <li>
                                        <a class="dropdown-item" href="#" @click="setProjectStatus(userProject, projectStatuses.COMPLETE)">
                                            <InfoToolTip :elId="getNewElUid()" :isHtmlContent="true" :content="CONTENT.completeStatusInfo"/>
                                            Complete
                                        </a>
                                    </li>
                                    <li>
                                        <a class="dropdown-item" href="#" @click="setProjectStatus(userProject, projectStatuses.HIDDEN)">
                                            <InfoToolTip :elId="getNewElUid()" :isHtmlContent="true" :content="CONTENT.hiddenStatusInfo"/>
                                            Hidden
                                        </a>
                                    </li>
                                </ul>
                            </div>
                        </template>
                    </BaseCard>
                    <div v-if="!initData.userProjects.length">
                        <a href="/candidateOnboard/">
                            Find a project to get started
                        </a>
                    </div>
                </div>
            </div>
            <div class="col-md-9 card-custom table-responsive-md">
                <h3>Applications</h3>
                <Table
                    class="mt-3"
                    :data="initData.jobApplications"
                    :headers="[
                        [
                            {},
                            {value: 'Employer', sortFn: 'job.employer'},
                            {value: 'Job title', sortFn: 'job.jobTitle'},
                            {value: 'Project', sortFn: 'userProject.customProject.projectTitle'},
                            {value: 'Status', sortFn: getApplicationStatus},
                        ]
                    ]"
                    emptyDataMessage="No job applications"
                >
                    <template v-slot:body>
                        <tr v-for="jobApplication in initData.jobApplications" class="hover-menu">
                            <td>
                                <HamburgerDropdown :elId="getNewElUid()">
                                    <li @click="eventBus.emit('open:editJobApplicationModal', jobApplication)">
                                        <a class="dropdown-item" href="#"><i class="fas fa-pencil-alt"></i> Edit application</a>
                                    </li>
                                </HamburgerDropdown>
                            </td>
                            <td>{{jobApplication.job.employer}}</td>
                            <td><a :href="`/job-posting/${jobApplication.job.id}/`">{{jobApplication.job.jobTitle}}</a></td>
                            <td>
                                <a :href="`/project/${jobApplication.userProject.customProject.projectId}/?${getCustomProjectQueryParams(jobApplication.userProject.customProject)}`">
                                    {{jobApplication.userProject.customProject.projectTitle}}
                                </a>
                            </td>
                            <td>{{getApplicationStatus(jobApplication)}}</td>
                        </tr>
                    </template>
                </Table>
            </div>
        </div>
    </div>
    <EditJobApplicationModal/>
    <EditUserProjectModal/>
</template>

<script>
import globalData, {PROJECT_STATUSES} from '../../../globalData';
import BadgesSkillLevels from "../../components/BadgesSkillLevels";
import BadgesSkills from "../../components/BadgesSkills";
import BannerAlert from "../../components/BannerAlert";
import BaseCard from "../../components/BaseCard";
import CONTENT from "./CandidateDashboardContent";
import dataUtil from "../../../utils/data";
import EditJobApplicationModal from "../../modals/EditJobApplicationModal";
import EditUserProjectModal from "../../modals/EditUserProjectModal";
import HamburgerDropdown from "../../components/HamburgerDropdown";
import InfoToolTip from "../../components/InfoToolTip";
import PageHeader from "../../components/PageHeader";
import skillLevelSelectize from "../../selectizeCfgs/skillLevels";
import Table from "../../components/Table";

export default {
    name: "CandidateDashboardPage",
    components: {
        BadgesSkillLevels, BadgesSkills, BannerAlert, BaseCard, EditJobApplicationModal, EditUserProjectModal,
        HamburgerDropdown, InfoToolTip, PageHeader, Table
    },
    data() {
        return {
            isUpdateData: true,
            CONTENT,
            projectStatuses: PROJECT_STATUSES
        }
    },
    methods: {
        capitalize: dataUtil.capitalize,
        getApplicationStatus: dataUtil.getApplicationStatus,
        getStartedApplications(project) {
            return this.initData.jobApplications.filter((app) => {
                return (
                    app.userProject.id === project.id
                    && !app.submissionDateTime
                    && !app.withdrawDateTime
                    && !app.approveDateTime
                    && !app.declineDateTime
                )
            });
        },
        getAppliedApplications(project) {
            return this.initData.jobApplications.filter((app) => {
                return (
                    app.userProject.id === project.id
                    && app.submissionDateTime
                    && !app.withdrawDateTime
                    && !app.approveDateTime
                    && !app.declineDateTime
                )
            });
        },
        getSelectedApplications(project) {
            return this.initData.jobApplications.filter((app) => {
                return (
                    app.userProject.id === project.id
                    && app.approveDateTime
                )
            });
        },
        getDeclinedApplications(project) {
            return this.initData.jobApplications.filter((app) => {
                return (
                    app.userProject.id === project.id
                    && app.declineDateTime
                )
            });
        },
        getCustomProjectQueryParams(customProject) {
            let queryString = `skillLevel=${customProject.skillLevelBit}`;
            customProject.skills.forEach((s) => {
                queryString += `&skill=${s.id}`;
            });
            return queryString;
        },
        resetAjaxData() {
            this.crudUrl = null;
            this.initDataKey = null;
            this.formData = {}
        },
        setProjectStatus(userProject, status) {
            this.crudUrl = 'user-project/status/';
            this.initDataKey = 'userProjects';
            this.formData = {
                id: userProject.id,
                status
            };
            if (status === this.globalData.PROJECT_STATUSES.COMPLETE && !window.confirm(
                `Are you sure you sure you want to finalize this project? You will not be able to edit it for the next ${this.pluralize('day', this.globalData.PROJECT_COMPLETE_LOCK_DAYS)}.`
            )) {
                this.resetAjaxData();
                return;
            }
            this.readAndSubmitForm();
            this.resetAjaxData();
        }
    },
    mounted() {
        this.initData.userProjects.forEach((up) => {
            skillLevelSelectize.setSkillLevels([up.customProject], true);
        });
    }
}
</script>