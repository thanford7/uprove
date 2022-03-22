<template>
    <BasePage headerTitle="Dashboard" :headerImage="initData.user.profileImage">
        <div class="row mb-3 justify-content-center">
            <div class="col-md-9 card-custom table-responsive-md">
                <h4 style="display: inline-block">Projects</h4>
                <div class="row justify-content-center mt-2">
                    <BaseCard
                        v-for="userProject in initData.userProjects"
                        :cardItem="userProject"
                        :elId="getNewElUid()"
                        :isShowViewMoreLink="false"
                    >
                        <template v-slot:outer>
                            <div class="badge badge-top -color-darkblue">{{userProject.customProject.role}}</div>
                        </template>
                        <template v-slot:header>
                            {{userProject.customProject.projectTitle}}
                            <span
                                v-if="userProject.files.length"
                                class="fa-stack fa-stack-sm float-end"
                                :title="`${pluralize('file', getFileCount(userProject))} uploaded`"
                            >
                              <i class="fas fa-file fa-stack-2x"></i>
                              <strong class="fa-stack-1x -color-white-text">{{getFileCount(userProject)}}</strong>
                            </span>
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
                                <a :href="`/project/${userProject.customProject.projectId}/?${getCustomProjectQueryParams(userProject.customProject)}`" target="_blank">
                                    <i class="fas fa-external-link-alt"></i>
                                    View project instructions
                                </a>
                            </div>
                            <div>
                                <div
                                    class="form-check form-switch mt-2"
                                    :title="getProjectCompleteLockedNote(userProject)"
                                >
                                  <input class="form-check-input" type="checkbox" id="projectStatus"
                                         :checked="(userProject.status === globalData.PROJECT_STATUSES.COMPLETE)"
                                         @change="toggleProjectComplete(userProject, $event)"
                                    :disabled="userProject.isLocked || !userProject.files.length"
                                  >
                                  <label class="form-check-label" for="projectStatus">
                                      <span v-if="userProject.isLocked"><i class="fas fa-lock"></i>&nbsp;</span>
                                      <InfoToolTip :elId="getNewElUid()" :isHtmlContent="true" :content="CONTENT.draftStatusInfo + CONTENT.completeStatusInfo"/>
                                      Project complete
                                  </label>
                                </div>
                                <div class="form-check form-switch mt-2">
                                  <input class="form-check-input" type="checkbox" id="projectHidden"
                                         :checked="userProject.isHidden"
                                         @change="toggleProjectHidden(userProject, $event)"
                                  >
                                  <label class="form-check-label" for="projectHidden">
                                      <InfoToolTip :elId="getNewElUid()" :isHtmlContent="true" :content="CONTENT.hiddenStatusInfo"/>
                                      Project hidden
                                  </label>
                                </div>
                                <div class="mt-2">
                                    <button
                                        class="btn btn-primary btn-sm"
                                        :class="(userProject.isLocked) ? 'w-75' : 'w-100'"
                                        @click="eventBus.emit('open:editUserProjectModal', userProject)"
                                        :disabled="userProject.isLocked"
                                        :title="getProjectLockedNote(userProject)"
                                    >
                                        Edit project files
                                    </button>
                                    <span v-if="userProject.isLocked">
                                        &nbsp;
                                        <ButtonDelete
                                            class="btn-sm"
                                            @click="deleteProject(userProject)"
                                        />
                                    </span>
                                </div>
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
            <div v-if="initData.jobApplications && initData.jobApplications.length" class="col-md-9 card-custom table-responsive-md">
                <h4>Applications</h4>
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
            <div class="col-md-9 card-custom">
                <h4>Resources</h4>
                <div v-if="initData.user.videos && initData.user.videos.length" class="row">
                    <h5>Videos</h5>
                    <div v-for="video in initData.user.videos"
                         class="col-md-5 m-2 p-2 -hover-highlight-border"
                         style="position: relative;"
                    >
                        <div>
                            <h6>{{video.title}}</h6>
                            <video controls :src="video.video"></video>
                        </div>
                        <ButtonDelete class="-absolute-top-right -absolute-top-right-padded"
                                      :isSmall="true"
                                      @click="deleteVideo(video.id)"
                        />
                    </div>
                </div>
                <div v-if="initData.user.images && initData.user.images.length" class="row">
                    <h5>Images</h5>
                    <div v-for="image in initData.user.images"
                         class="col-md-5 m-2 p-2 -hover-highlight-border"
                         style="position: relative;"
                    >
                        <div>
                            <h6>{{image.title}}</h6>
                            <img :src="image.image">
                        </div>
                        <ButtonDelete class="-absolute-top-right -absolute-top-right-padded"
                                      :isSmall="true"
                                      @click="deleteImage(image.id)"
                        />
                    </div>
                </div>
                <div v-if="initData.user.files && initData.user.files.length" class="row">
                    <h5>Files</h5>
                    <div v-for="file in initData.user.files" class="col-6 col-md-4 m-2 -hover-highlight-border">
                        <div>
                            <FileDisplay :file="file"/>
                            <ButtonDelete :isSmall="true" @click="deleteFile(file.id)"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </BasePage>
    <AddVideoRecordingModal/>
    <EditJobApplicationModal/>
    <EditUserProjectModal/>
</template>

<script>
import {PROJECT_STATUSES} from '../../../globalData';
import AddVideoRecordingModal from "../../modals/AddVideoRecordingModal";
import BadgesSkillLevels from "../../components/BadgesSkillLevels";
import BadgesSkills from "../../components/BadgesSkills";
import BannerAlert from "../../components/BannerAlert";
import BaseCard from "../../components/BaseCard";
import ButtonDelete from "../../buttons/ButtonDelete";
import CONTENT from "./CandidateDashboardContent";
import dataUtil from "../../../utils/data";
import EditJobApplicationModal from "../../modals/EditJobApplicationModal";
import EditUserProjectModal from "../../modals/EditUserProjectModal";
import FileDisplay from "../../components/FileDisplay";
import HamburgerDropdown from "../../components/HamburgerDropdown";
import InfoToolTip from "../../components/InfoToolTip";
import PageHeader from "../../components/PageHeader";
import skillLevelSelectize from "../../selectizeCfgs/skillLevels";
import Table from "../../components/Table";
import userProjectUtil from "../../../utils/userProject";
import BasePage from "../BasePage";

export default {
    name: "CandidateDashboardPage",
    components: {
        BasePage, AddVideoRecordingModal, BadgesSkillLevels, BadgesSkills, BannerAlert, BaseCard, ButtonDelete,
        EditJobApplicationModal, EditUserProjectModal, FileDisplay, HamburgerDropdown, InfoToolTip, PageHeader, Table
    },
    data() {
        return {
            isUpdateData: true,
            confirmDelete: false,  // Delete confirmation is done directly in this file
            initDataKey: null,  // Set when ajax method is called
            customDeleteFn: null,  // Once files are deleted, they need to be removed from user projects as well
            CONTENT,
            projectStatuses: PROJECT_STATUSES
        }
    },
    methods: {
        capitalize: dataUtil.capitalize,
        getApplicationStatus: dataUtil.getApplicationStatus,
        getProjectLockedNote: userProjectUtil.getProjectLockedNote,
        getProjectCompleteLockedNote: userProjectUtil.getProjectCompleteLockedNote,
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
            this.formData = {};
            this.customDeleteFn = null;
        },
        afterUpdateInitData() {
            this.resetAjaxData()
        },
        afterDeleteInitData() {
            if (this.customDeleteFn) {
                this.customDeleteFn();
            }
            this.resetAjaxData();
        },
        updateUserProjects(removeId, removeKey) {
            this.initData.userProjects.forEach((up) => {
                up[removeKey] = up[removeKey].filter((item) => item.id !== removeId);
            });
        },
        deleteVideo(videoId) {
            this.crudUrl = 'user-video/';
            this.initDataKey = 'user.videos';
            this.formData = {id: videoId};
            this.customDeleteFn = () => this.updateUserProjects(videoId, 'videos');
            if (window.confirm('Are you sure you want to delete this video? It will be permanently deleted and removed from any projects that reference it.')) {
                this.deleteObject();
            }
        },
        deleteImage(imageId) {
            this.crudUrl = 'user-image/';
            this.initDataKey = 'user.images';
            this.formData = {id: imageId};
            this.customDeleteFn = () => this.updateUserProjects(videoId, 'images');
            if (window.confirm('Are you sure you want to delete this image? It will be permanently deleted and removed from any projects that reference it.')) {
                this.deleteObject();
            }
        },
        deleteFile(fileId) {
            this.crudUrl = 'user-file/';
            this.initDataKey = 'user.files';
            this.formData = {id: fileId};
            this.customDeleteFn = () => this.updateUserProjects(videoId, 'files');
            if (window.confirm('Are you sure you want to delete this file? It will be permanently deleted and removed from any projects that reference it.')) {
                this.deleteObject();
            }
        },
        deleteProject(userProject) {
            this.crudUrl = 'user-project/';
            this.initDataKey = 'userProjects';
            this.formData = {id: userProject.id};
            if (window.confirm('Are you sure you want to delete this project? This will withdraw any job applications where you use this project.')) {
                this.deleteObject();
            }
        },
        getFileCount(userProject) {
            return userProject.videos.length + userProject.images.length + userProject.files.length;
        },
        toggleProjectComplete(userProject, e) {
            this.crudUrl = 'user-project/status/';
            this.initDataKey = ['userProjects', 'jobApplications'];
            const isChecked = e.returnValue;
            this.formData = {
                id: userProject.id,
                status: (isChecked) ? this.globalData.PROJECT_STATUSES.COMPLETE : this.globalData.PROJECT_STATUSES.DRAFT
            };
            if (isChecked && !window.confirm(
                `Are you sure you sure you want to finalize this project? You will not be able to edit it for the next ${this.pluralize('day', this.globalData.PROJECT_COMPLETE_LOCK_DAYS)}.`
            )) {
                this.resetAjaxData();
                $(e.currentTarget).prop('checked', false);
                return;
            }
            if (userProject.jobApplicationCount && window.confirm(`Do you want to submit the ${this.pluralize('application', userProject.jobApplicationCount)} associated with this project? You can always submit each application later using the applications section in your dashboard.`)) {
                this.formData.isSubmitApplications = true;
            }
            this.readAndSubmitForm();
        },
        toggleProjectHidden(userProject, e) {
            this.crudUrl = 'user-project/status/';
            this.initDataKey = 'userProjects';
            this.formData = {
                id: userProject.id,
                isHidden: e.returnValue
            };
            this.readAndSubmitForm();
        }
    },
    mounted() {
        this.initData.userProjects.forEach((up) => {
            skillLevelSelectize.setSkillLevels([up.customProject], true);
        });
    }
}
</script>