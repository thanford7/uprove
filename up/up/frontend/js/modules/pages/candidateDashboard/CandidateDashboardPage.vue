<template>
    <div class="container-lg">
        <BannerAlert/>
        <PageHeader title="Dashboard" :image="initData.user.profileImage"/>
        <div class="row mb-3 justify-content-center">
            <div class="col-md-9 card-custom table-responsive-md">
                <h3 style="display: inline-block">Projects</h3>
                <Table
                    class="mt-3"
                    :data="initData.userProjects"
                    :headers="[
                        [{colspan: 2}, {value: 'Employers', colspan: 4, classes: 'text-center border-start'}],
                        [
                            {},
                            {value: 'Project', sortFn: 'customProject.projectTitle'},
                            {value: 'Started', toolTip: TOOLTIPS.candidateStarted, classes: 'text-center border-start'},
                            {value: 'Applied', toolTip: TOOLTIPS.candidateApplied, classes: 'text-center'},
                            {value: 'Selected', toolTip: TOOLTIPS.candidateSelected, classes: 'text-center'},
                            {value: 'Declined', toolTip: TOOLTIPS.candidateDeclined, classes: 'text-center'}
                        ]
                    ]"
                    emptyDataMessage="<a href='/projects/'>Find a project to get started</a>"
                >
                    <template v-slot:body>
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
                    </template>
                </Table>
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
import BannerAlert from "../../components/BannerAlert";
import dataUtil from "../../../utils/data";
import EditJobApplicationModal from "../../modals/EditJobApplicationModal";
import EditUserProjectModal from "../../modals/EditUserProjectModal";
import HamburgerDropdown from "../../components/HamburgerDropdown";
import InfoToolTip from "../../components/InfoToolTip";
import PageHeader from "../../components/PageHeader";
import Table from "../../components/Table";

export default {
    name: "CandidateDashboardPage",
    components: {
        BannerAlert, EditJobApplicationModal, EditUserProjectModal, HamburgerDropdown, InfoToolTip,
        PageHeader, Table
    },
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