<template>
    <div class="container-lg">
        <BannerAlert/>
        <div class="row mt-3 mb-3">
            <div class="align-items-center" style="display: flex">
                <img v-if="initData.user.profileImage" :src="initData.user.profileImage" alt="" class="employer-logo">
                <h2 style="display: inline-block; margin-bottom: 0">Dashboard</h2>
            </div>
        </div>
        <div class="row mb-3 justify-content-center">
            <div class="col-md-9 card-custom table-responsive-md">
                <h3 style="display: inline-block">Projects</h3>
                <table class="table mt-3">
                    <thead>
                        <tr>
                            <th colspan="2"></th>
                            <th colspan="4" class="text-center border-start">Employers</th>
                        </tr>
                        <tr>
                            <th></th>
                            <th>Project</th>
                            <th class="text-center border-start">Started <InfoToolTip :content="TOOLTIPS.candidateStarted" :elId="getNewElUid()"/></th>
                            <th class="text-center">Applied <InfoToolTip :content="TOOLTIPS.candidateApplied" :elId="getNewElUid()"/></th>
                            <th class="text-center">Selected <InfoToolTip :content="TOOLTIPS.candidateSelected" :elId="getNewElUid()"/></th>
                            <th class="text-center">Declined <InfoToolTip :content="TOOLTIPS.candidateDeclined" :elId="getNewElUid()"/></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="userProject in initData.userProjects" class="hover-menu">
                            <td>
                                <HamburgerDropdown :elId="getNewElUid()">
                                    <li @click="eventBus.emit('open:editUserProjectModal', userProject)">
                                        <a class="dropdown-item" href="#"><i class="fas fa-pencil-alt"></i> Edit project</a>
                                    </li>
                                </HamburgerDropdown>
                            </td>
                            <td>
                                <a :href="`/project/${userProject.customProject.projectId}/?${getCustomProjectQueryParams(userProject.customProject)}`">
                                    {{userProject.customProject.projectTitle}}
                                </a>
                            </td>
                            <td class="text-center border-start">{{getStartedApplications(userProject).length}}</td>
                            <td class="text-center">{{getAppliedApplications(userProject).length}}</td>
                            <td class="text-center">{{getSelectedApplications(userProject).length}}</td>
                            <td class="text-center">{{getDeclinedApplications(userProject).length}}</td>
                        </tr>
                        <tr v-if="!initData.userProjects.length">
                            <td colspan="6"><a href="/projects/">Find a project to get started</a></td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="col-md-9 card-custom table-responsive-md">
                <h3>Applications</h3>
                <table class="table mt-3">
                    <thead>
                        <tr>
                            <th></th>
                            <th>Employer</th>
                            <th>Job Title</th>
                            <th>Project</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
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
                        <tr v-if="!initData.userProjects.length">
                            <td colspan="5">No job applications</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    <EditJobApplicationModal/>
    <EditUserProjectModal/>
</template>

<script>
import BannerAlert from "../../components/BannerAlert";
import EditJobApplicationModal from "../../modals/EditJobApplicationModal";
import EditUserProjectModal from "../../modals/EditUserProjectModal";
import HamburgerDropdown from "../../components/HamburgerDropdown";
import InfoToolTip from "../../components/InfoToolTip";
import dataUtil from "../../../utils/data";

export default {
    name: "CandidateDashboardPage",
    components: {BannerAlert, EditJobApplicationModal, EditUserProjectModal, HamburgerDropdown, InfoToolTip},
    methods: {
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
        }
    }
}
</script>