<template>
    <BasePage :headerTitle="`${initData.employer.companyName} Dashboard`" :headerImage="initData.employer.logo">
        <div class="row mb-3 justify-content-center">
            <div class="col-md-9 card-custom table-responsive-md">
                <h3 style="display: inline-block">Job postings</h3>
                <button type="button" class="btn btn-primary float-end" @click="eventBus.emit('open:editJobPostingModal')">
                    Create job posting
                </button>
                <Table
                    class="mt-3"
                    :data="initData.employer.jobs"
                    :headers="[
                        [{colspan: 3}, {value: 'Applicants', colspan: 4, classes: 'text-center border-start'}],
                        [
                            {},
                            {value: 'Job title', sortFn: 'jobTitle'},
                            {value: 'Status', sortFn: getJobStatus},
                            {value: 'Invited', classes: 'text-center border-start'},
                            {value: 'Applied', classes: 'text-center'},
                            {value: 'Selected', classes: 'text-center'},
                            {value: 'Declined', classes: 'text-center'}
                        ]
                    ]"
                    emptyDataMessage="Post your first job"
                >
                    <template v-slot:body>
                        <tr v-for="job in initData.employer.jobs" class="hover-menu">
                            <td>
                                <HamburgerDropdown :elId="getNewElUid()">
                                    <li>
                                        <a class="dropdown-item" href="#" @click="eventBus.emit('open:editJobPostingModal', job)">
                                            <i class="fas fa-pencil-alt"></i> Edit job
                                        </a>
                                    </li>
                                    <li>
                                        <a class="dropdown-item" href="#" @click="eventBus.emit('open:inviteJobApplicantModal', job)">
                                            <i class="fas fa-user-plus"></i> Invite applicants
                                        </a>
                                    </li>
                                </HamburgerDropdown>
                            </td>
                            <td title="View job posting"><a :href="`/job-posting/${job.id}/`">{{job.jobTitle}}</a></td>
                            <td>{{getJobStatus(job)}}</td>
                            <td class="text-center border-start">{{job.applications.filter((a) => !Boolean(a.submissionDateTime)).length}}</td>
                            <td class="text-center">{{job.applications.filter((a) => Boolean(a.submissionDateTime)).length}}</td>
                            <td class="text-center">{{job.applications.filter((a) => Boolean(a.approveDateTime)).length}}</td>
                            <td class="text-center">{{job.applications.filter((a) => Boolean(a.declineDateTime)).length}}</td>
                        </tr>
                    </template>
                </Table>
            </div>
            <div class="col-md-9 card-custom table-responsive-md">
                <h3>Applications</h3>
                <Table
                    class="mt-3"
                    :data="applications"
                    :headers="[
                        [
                            {},
                            {value: 'First name', sortFn: 'user.firstName'},
                            {value: 'Last name', sortFn: 'user.lastName'},
                            {value: 'Status', sortFn: getApplicationStatus},
                            {value: 'Job title', sortFn: 'job.jobTitle'},
                            {value: 'Project', sortFn: 'userProject.customProject.projectTitle'},
                        ]
                    ]"
                    emptyDataMessage="No job applications"
                >
                    <template v-slot:body>
                        <tr v-for="application in applications" class="hover-menu">
                            <td>
                                <HamburgerDropdown :elId="getNewElUid()">
                                    <li>
                                        <a class="dropdown-item" href="#"><i class="far fa-envelope"></i> Message</a>
                                    </li>
                                    <li
                                        v-if="getApplicationStatus(application) !== APPLICATION_STATUS.NOT_SUBMITTED"
                                        @click="eventBus.emit('open:viewCandidateApplicationModal', application)"
                                    >
                                        <a class="dropdown-item" href="#">
                                            <i class="far fa-eye"></i> Quick view application
                                        </a>
                                    </li>
                                    <li @click="approveApplication(application)">
                                        <a class="dropdown-item" href="#">
                                            <i class="far fa-thumbs-up -color-green-text"></i> Approve <InfoToolTip :elId="getNewElUid()" :content="TOOLTIPS.employerApprove"/>
                                        </a>
                                    </li>
                                    <li @click="declineApplication(application)">
                                        <a class="dropdown-item" href="#">
                                            <i class="far fa-thumbs-down -color-red-text"></i> Decline <InfoToolTip :elId="getNewElUid()" :content="TOOLTIPS.employerDecline"/>
                                        </a>
                                    </li>
                                </HamburgerDropdown>
                            </td>
                            <td>{{application.user.firstName}}</td>
                            <td>{{application.user.lastName}}</td>
                            <td>{{getApplicationStatus(application)}}</td>
                            <td>{{application.job.jobTitle}}</td>
                            <td>{{application?.userProject?.customProject?.projectTitle || '-None-'}}</td>
                        </tr>
                    </template>
                </Table>
            </div>
            <div class="col-md-9 card-custom table-responsive-md">
                <h3>Linked projects</h3>
                <Table
                    class="mt-3"
                    :data="customProjects"
                    :headers="[
                        [
                            {},
                            {value: 'Project', sortFn: 'projectTitle'},
                            {value: 'Career level', sortFn: 'skillLevelBit'},
                            {value: 'Skills'},
                            {value: 'Linked jobs'},
                        ]
                    ]"
                    emptyDataMessage="<a href='/projects/'>Find a project to get started</a>"
                >
                    <template v-slot:body>
                        <tr v-for="customProject in customProjects" class="hover-menu">
                            <td>
                                <HamburgerDropdown :elId="getNewElUid()">
                                    <li @click="eventBus.emit('open:editCustomProjectModal', customProject)">
                                        <a class="dropdown-item" href="#"><i class="fas fa-pencil-alt"></i> Edit project</a>
                                    </li>
                                </HamburgerDropdown>
                            </td>
                            <td>{{customProject.projectTitle}}</td>
                            <td><BadgesSkillLevels :skillLevels="customProject.skillLevel"/></td>
                            <td><BadgesSkills :skills="customProject.skills"/></td>
                            <td>
                                <ul>
                                    <li v-for="job in customProject.jobs">{{job.jobTitle}}</li>
                                </ul>
                            </td>
                        </tr>
                    </template>
                </Table>
            </div>
            <div class="col-md-9 card-custom">
                <h3>Settings</h3>
                <div>
                    <a href="#" @click="eventBus.emit('open:editEmployerModal', initData.employer)">Edit employer information</a>
<!--                    <a href="#">Manage users</a>-->
<!--                    <a href="#">Update billing</a>-->
                </div>
            </div>
        </div>
    </BasePage>
    <EditCustomProjectModal/>
    <EditEmployerModal/>
    <EditJobPostingModal/>
    <InviteJobApplicantModal/>
    <ViewCandidateApplicationModal
        @approve="approveApplication($event)"
        @decline="declineApplication($event)"
    />
</template>

<script>
import dateUtil from "../../../utils/dateUtil";
import dataUtil, {APPLICATION_STATUS} from "../../../utils/data";
import dayjs from "dayjs/esm";
import BadgesSkillLevels from "../../components/BadgesSkillLevels";
import BadgesSkills from "../../components/BadgesSkills";
import BannerAlert from "../../components/BannerAlert";
import BasePage from "../BasePage";
import EditCustomProjectModal from "../../modals/EditCustomProjectModal";
import EditEmployerModal from "../../modals/EditEmployerModal";
import EditJobPostingModal from "../../modals/EditJobPostingModal";
import HamburgerDropdown from "../../components/HamburgerDropdown";
import InfoToolTip from "../../components/InfoToolTip";
import InviteJobApplicantModal from "../../modals/InviteJobApplicantModal";
import Table from "../../components/Table";
import ViewCandidateApplicationModal from "../../modals/ViewCandidateApplicationModal";

export default {
    name: "EmployerDashboardPage.vue",
    components: {
        BannerAlert, BadgesSkillLevels, BadgesSkills, BasePage, EditCustomProjectModal, EditEmployerModal,
        EditJobPostingModal, HamburgerDropdown, InfoToolTip, InviteJobApplicantModal,
        Table, ViewCandidateApplicationModal
    },
    data() {
        return {
            APPLICATION_STATUS,
            applications: null,
            customProjects: null,
            sortKeysJobPostingTable: []
        }
    },
    methods: {
        getApplicationStatus: dataUtil.getApplicationStatus,
        getJobStatus(job) {
            if (job.closeDate) {
                return 'CLOSED';
            }
            if (job.pauseDate) {
                return 'PAUSED';
            }
            if (job.openDate) {
                return 'OPEN'
            }
            return 'DRAFT';
        },
        approveApplication(application) {
            const ajaxData = this.getAjaxFormData({
                id: application.id,
                approveDateTime: dateUtil.serializeDateTime(dayjs())
            });
            this.submitAjaxRequest(ajaxData, {
                url: this.apiUrl + 'user-job-application/',
                success: (data) => {
                    const updateApp = this.applications.find((app) => app.id === application.id);
                    updateApp.approveDateTime = data.approveDateTime;
                    updateApp.declineDateTime = null;
                }
            });
        },
        declineApplication(application) {
            const ajaxData = this.getAjaxFormData({
                id: application.id,
                declineDateTime: dateUtil.serializeDateTime(dayjs())
            });
            this.submitAjaxRequest(ajaxData, {
                url: this.apiUrl + 'user-job-application/',
                success: (data) => {
                    const updateApp = this.applications.find((app) => app.id === application.id);
                    updateApp.approveDateTime = null;
                    updateApp.declineDateTime = data.declineDateTime;
                }
            });
        }
    },
    mounted() {
        this.applications = this.initData.employer.jobs.reduce((applications, job) => {
            return [...applications, ...job.applications.map((app) => {
                app.job = {
                    id: job.id,
                    jobTitle: job.jobTitle
                };
                return app;
            })];
        }, []);

        this.customProjects = this.initData.employer.jobs.reduce((customProjects, job) => {
            job.allowedProjects.forEach((ap) => {
                if (ap.id in customProjects) {
                    customProjects[ap.id].jobs.push({id: job.id, jobTitle: job.jobTitle});
                } else {
                    ap.jobs = [{id: job.id, jobTitle: job.jobTitle}];
                    ap.skillLevel = this.getSkillLevelsFromBits(ap.skillLevelBit);
                    customProjects[ap.id] = ap;
                }
            });
            return customProjects;
        }, {});
        this.customProjects = Object.values(this.customProjects);
    }
}
</script>