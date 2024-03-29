<template>
    <BasePage>
        <div class="row mb-3 justify-content-center">
            <div class="col-md-8">
                <ul class="nav nav-tabs" id="candidateTabs" role="tablist">
                    <li class="nav-item">
                        <button
                            class="nav-link" id="projects-tab"
                            :class="(currentTab === 'projects') ? 'active': ''"
                            data-bs-toggle="tab" data-bs-target="#projects"
                            type="button" role="tab" aria-selected="true"
                            @click="setTabParam('projects')"
                        >Projects
                        </button>
                    </li>
                    <li class="nav-item">
                        <button
                            class="nav-link" id="applications-tab"
                            :class="(currentTab === 'applications') ? 'active': ''"
                            data-bs-toggle="tab" data-bs-target="#applications"
                            type="button" role="tab" aria-selected="false"
                            @click="setTabParam('applications')"
                        >Applications
                        </button>
                    </li>
                    <li class="nav-item">
                        <button
                            class="nav-link" id="resources-tab"
                            :class="(currentTab === 'resources') ? 'active': ''"
                            data-bs-toggle="tab" data-bs-target="#resources"
                            type="button" role="tab" aria-selected="false"
                            @click="setTabParam('resources')"
                        >Uploads
                        </button>
                    </li>
                </ul>
                <div class="tab-content mb-3" id="candidateTabContent">
                    <div class="tab-pane fade" :class="(currentTab === 'projects') ? 'show active': ''" id="projects"
                         role="tabpanel">
                        <div class="row justify-content-center mt-2">
                            <div v-for="userProject in initData.userProjects" class="mb-3">
                                <h6 class="after-border-middle d-flex align-items-center fw-bolder">
                                    {{ userProject.customProject.projectTitle }}
                                </h6>
                                <div class="mb-2">
                                    <div class="mt-2 me-2" style="display: inline-block">
                                        <button
                                            class="btn btn-primary btn-sm"
                                            @click="eventBus.emit('open:editUserProjectModal', userProject)"
                                        >
                                            Edit project
                                        </button>
                                    </div>
                                    <div
                                        class="form-check form-switch mt-2 me-2"
                                        :title="getProjectCompleteLockedNote(userProject)"
                                        style="display: inline-block"
                                    >
                                        <input class="form-check-input" type="checkbox" id="projectStatus"
                                               :checked="(userProject.status === globalData.PROJECT_STATUSES.COMPLETE)"
                                               @change="toggleProjectComplete(userProject, $event)"
                                               :disabled="!getFileCount(userProject)"
                                        >
                                        <label class="form-check-label" for="projectStatus">
                                            <InfoToolTip :elId="getNewElUid()" :isHtmlContent="true"
                                                         :content="CONTENT.draftStatusInfo + CONTENT.completeStatusInfo"/>
                                            Project complete
                                        </label>
                                    </div>
                                    <div class="form-check form-switch mt-2" style="display: inline-block">
                                        <input class="form-check-input" type="checkbox"
                                               :checked="userProject.isHidden"
                                               @change="toggleProjectHidden(userProject, $event)"
                                        >
                                        <label class="form-check-label">
                                            <InfoToolTip :elId="getNewElUid()" :isHtmlContent="true"
                                                         :content="CONTENT.hiddenStatusInfo"/>
                                            Project hidden
                                        </label>
                                    </div>
                                </div>
                                <BadgesSkills :skills="userProject.customProject.skills"/>
                                <div class="mt-2">
                                    <div class="-color-moderategrey-text" v-html="userProject.customProject.projectDescription"></div>
                                </div>
                                <div>
                                    <a :href="`/project/${userProject.customProject.projectId}/?${getCustomProjectQueryParams(userProject.customProject)}`"
                                       target="_blank">
                                        <i class="fas fa-external-link-alt"></i>
                                        View project instructions
                                    </a>
                                </div>
                                <div v-if="getFileCount(userProject)" class="mt-2">
                                    <h6>Files</h6>
                                    <div v-for="file in getAllFiles(userProject)">
                                        <FileDisplay
                                            :file="file"
                                        />
                                    </div>
                                </div>
                            </div>
                            <div v-if="!initData.userProjects.length">
                                <a href="/projects/">
                                    Find a project to get started
                                </a>
                            </div>
                        </div>
                    </div>
                    <div class="tab-pane fade" :class="(currentTab === 'applications') ? 'show active': ''"
                         id="applications" role="tabpanel">
                        <div
                            class="table-responsive-md"
                        >
                            <Table
                                class="mt-3 align-middle"
                                :data="initData.jobApplications"
                                :headers="[
                        [
                            {value: 'Action'},
                            {value: 'Employer', sortFn: 'job.employer'},
                            {value: 'Job title', sortFn: 'job.jobTitle'},
                            {value: 'Status', sortFn: getApplicationStatus},
                        ]
                    ]"
                                emptyDataMessage="No job applications. <a href='/jobs/'>Search jobs</a> to get started."
                            >
                                <template v-slot:body>
                                    <tr v-for="jobApplication in initData.jobApplications" class="hover-menu">
                                        <td>
                                            <button
                                                v-if="canApply(jobApplication)"
                                                class="btn btn-sm btn-outline-success -color-black-text"
                                                @click="updateAppSubmission(jobApplication, true)"
                                            >
                                                <i class="fas fa-file-import"></i> Apply
                                            </button>
                                            <button
                                                v-else
                                                class="btn btn-sm btn-outline-danger -color-black-text"
                                                @click="updateAppSubmission(jobApplication, false)"
                                            >
                                                <i class="fas fa-backspace"></i> Withdraw
                                            </button>
                                        </td>
                                        <td>{{ jobApplication.employer }}</td>
                                        <td><a
                                            :href="`/job-posting/${jobApplication.job.id}/`">{{
                                                jobApplication.job.jobTitle
                                            }}</a>
                                        </td>
                                        <td><ApplicationStatus :application="jobApplication"/></td>
                                    </tr>
                                </template>
                            </Table>
                        </div>
                    </div>
                    <div class="tab-pane fade" :class="(currentTab === 'resources') ? 'show active': ''"
                         id="resources" role="tabpanel">
                        <div
                            v-if="!initData.user.videos?.length && !initData.user.images?.length && !initData.user.files?.length">
                            No current uploads
                        </div>
                        <div v-if="initData.user.videos?.length" class="row justify-content-around mt-3">
                            <template
                                v-for="file in [...initData.user.videos, ...initData.user.images, ...initData.user.files]">
                                <div class="col-md-6 col-12 mb-3">
                                    <h6 class="text-center project-item-title">
                                        <FileDisplay :file="file"/>
                                        <i
                                            class="fas fa-trash -color-red-text"
                                            @click="deleteFile(file.id, file.type)"
                                            style="cursor: pointer;"
                                        ></i>
                                    </h6>
                                    <div class="project-item d-flex align-items-center justify-content-center">
                                        <video v-if="file.type === CONTENT_TYPES.VIDEO" controls :src="file.video"/>
                                        <img v-if="file.type === CONTENT_TYPES.IMAGE" :src="file.image"
                                             class="project-file-image">
                                        <img v-if="file.type === CONTENT_TYPES.FILE && file.thumbnail"
                                             :src="file.thumbnail" class="project-file-image">
                                        <div v-if="file.type === CONTENT_TYPES.FILE && !file.thumbnail" class="p-2">
                                            <div class="text-center"><i class="fas fa-file fa-4x"></i></div>
                                            <div class="-text-medium" style="margin: 0 auto;">No file image available
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </template>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card-custom card-custom--no-side-margin">
                    <h5 class="mb-3">Job suggestions</h5>
                    <div v-for="job in cData.jobSuggestions" class="row mb-2">
                        <div class="mb-2 d-flex align-items-center -border-top--blue -border-bottom--light">
                            <h6 class="mb-0 pt-2 pb-2"><a :href="`/job-posting/${job.id}`">{{ job.jobTitle }}</a></h6>
                            <FastApplyBtn v-if="job.isClient" :job="job" class="-pull-right" btnClasses="mt-1 mb-1"/>
                        </div>
                        <div class="col-3">
                            <img v-if="job.employerLogo" :src="job.employerLogo" class="logo">
                            <i v-else class="far fa-building fa-4x"></i>
                        </div>
                        <div class="col-6">
                            <h6>{{ job.companyName }}</h6>
                            <h6>{{ getLocationStr(job) }}</h6>
                        </div>
                    </div>
                    <div v-if="!cData?.jobSuggestions?.length">
                        No current job suggestions.
                        <a href="#"
                           @click="eventBus.emit('open:editJobPreferencesModal', initData.user.preferences)"
                        >Update your job preferences</a> to find great matches!
                    </div>
                </div>
            </div>
        </div>
        <canvas class="confetti"></canvas>
    </BasePage>
    <AddVideoRecordingModal/>
    <CelebrationModal/>
    <EditJobPreferencesModal/>
    <EditUserProjectModal/>
</template>

<script>
import {APPLICATION_STATUS_KEYS, CONTENT_TYPES, PROJECT_STATUSES} from '../../../globalData';
import AddVideoRecordingModal from "../../modals/AddVideoRecordingModal";
import ApplicationStatus from "../employerDashboard/ApplicationStatus";
import BadgesSkills from "../../components/BadgesSkills";
import BannerAlert from "../../components/BannerAlert";
import BaseCard from "../../components/BaseCard";
import ButtonDelete from "../../buttons/ButtonDelete";
import CelebrationModal from "../../modals/CelebrationModal";
import CONTENT from "./CandidateDashboardContent";
import dataUtil from "../../../utils/data";
import EditJobPreferencesModal from "../../modals/EditJobPreferencesModal";
import EditUserProjectModal from "../../modals/EditUserProjectModal";
import FastApplyBtn from "../jobs/FastApplyBtn";
import FileDisplay from "../../components/FileDisplay";
import HamburgerDropdown from "../../components/HamburgerDropdown";
import InfoToolTip from "../../components/InfoToolTip";
import PageHeader from "../../components/PageHeader";
import skillLevelSelectize from "../../selectizeCfgs/skillLevels";
import Table from "../../components/Table";
import userProjectUtil from "../../../utils/userProject";
import BasePage from "../base/BasePage";
import jobUtil from "../../../utils/jobs";
import UprovePartner from "../jobs/UprovePartner";
import dateUtil from "../../../utils/dateUtil";
import dayjs from "dayjs/esm";

export default {
    name: "CandidateDashboardPage",
    components: {
        UprovePartner,
        BasePage,
        AddVideoRecordingModal,
        ApplicationStatus,
        BadgesSkills,
        BannerAlert,
        BaseCard,
        ButtonDelete,
        CelebrationModal,
        EditJobPreferencesModal,
        EditUserProjectModal,
        FastApplyBtn,
        FileDisplay,
        HamburgerDropdown,
        InfoToolTip,
        PageHeader,
        Table
    },
    data() {
        return {
            isHardRefresh: true,
            confirmDelete: false,  // Delete confirmation is done directly in this file
            CONTENT,
            CONTENT_TYPES,
            projectStatuses: PROJECT_STATUSES,
            loadRoutes: [{route: 'user-job-rec/', dataKey: 'jobSuggestions'}],
        }
    },
    methods: {
        capitalize: dataUtil.capitalize,
        getLocationStr: jobUtil.getLocationStr,
        getProjectCompleteLockedNote: userProjectUtil.getProjectCompleteLockedNote,
        canApply(app) {
            return [
                APPLICATION_STATUS_KEYS.INVITED,
                APPLICATION_STATUS_KEYS.WITHDRAWN
            ].includes(app.status);
        },
        getCustomProjectQueryParams(customProject) {
            let queryString = `skillLevel=${customProject.skillLevelBit}`;
            customProject.skills.forEach((s) => {
                queryString += `&skill=${s.id}`;
            });
            return queryString;
        },
        deleteFile(fileId, fileType) {
            this.resetAjaxSettings();
            if (fileType === this.CONTENT_TYPES.FILE) {
                this.crudUrl = 'user-file/';
            } else if (fileType === this.CONTENT_TYPES.IMAGE) {
                this.crudUrl = 'user-image/';
            } else if (fileType === this.CONTENT_TYPES.VIDEO) {
                this.crudUrl = 'user-video/';
            }
            this.formData = {id: fileId};
            if (window.confirm(`Are you sure you want to delete this ${fileType}? It will be permanently deleted and removed from any projects that reference it.`)) {
                this.deleteObject();
            }
        },
        updateAppSubmission(app, isSubmit) {
            this.resetAjaxSettings();
            this.crudUrl = 'user-job-application/';
            this.formData.userId = this.initData.user.id;
            this.formData.id = app.id;
            if (isSubmit) {
                this.formData.applicationDateTime = dateUtil.serializeDateTime(dayjs());
                this.formData.withdrawDateTime = null;
            } else {
                this.formData.applicationDateTime = null;
                this.formData.withdrawDateTime = dateUtil.serializeDateTime(dayjs());
            }
            this.readAndSubmitForm();
        },
        getAllFiles(userProject) {
            return [...userProject.videos, ...userProject.images, ...userProject.files];
        },
        getFileCount(userProject) {
            return userProject.videos.length + userProject.images.length + userProject.files.length;
        },
        resetAjaxSettings() {
            this.isHardRefresh = true;
            this.isUpdateData = false;
            this.initDataKey = null;
        },
        toggleProjectComplete(userProject, e) {
            this.crudUrl = 'user-project/status/';
            this.isUpdateData = true;
            this.initDataKey = ['userProjects', 'jobApplications'];
            this.isHardRefresh = false;
            const isChecked = $(e.currentTarget).prop('checked');
            this.formData = {
                id: userProject.id,
                status: (isChecked) ? this.globalData.PROJECT_STATUSES.COMPLETE : this.globalData.PROJECT_STATUSES.DRAFT
            };

            this.afterUpdateInitData = () => {
                if (!isChecked) {
                    return;
                }
                this.eventBus.emit('open:celebrationModal', {
                    msg: 'Congratulations on completing a project!'
                });
            }
            this.readAndSubmitForm();
        },
        toggleProjectHidden(userProject, e) {
            this.resetAjaxSettings();
            this.crudUrl = 'user-project/status/';
            const isChecked = $(e.currentTarget).prop('checked');
            this.formData = {
                id: userProject.id,
                isHidden: isChecked
            };
            this.readAndSubmitForm();
        }
    },
    mounted() {
        this.initData.userProjects.forEach((up) => {
            skillLevelSelectize.setSkillLevels([up.customProject], true);
        });
        this.currentTab = 'projects';
        this.setTabFromParams();
    },
    async created() {
        await this.loadData();
    }
}
</script>