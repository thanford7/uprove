<template>
    <div class="container-lg">
        <BannerAlert/>
        <div class="row mt-3 mb-3">
            <div class="align-items-center" style="display: flex">
                <img v-if="initData.employer.logo" :src="initData.employer.logo" alt="" class="employer-logo">
                <h2 style="display: inline-block; margin-bottom: 0">{{initData.employer.companyName}} Dashboard</h2>
            </div>
        </div>
        <div class="row mb-3 justify-content-center">
            <div class="col-md-9 card-custom table-responsive-md">
                <h3 style="display: inline-block">Job postings</h3>
                <button type="button" class="btn btn-primary float-end" @click="eventBus.emit('open:editJobPostingModal')">
                    Create job posting
                </button>
                <table class="table mt-3">
                    <thead>
                        <tr>
                            <th colspan="3"></th>
                            <th colspan="4" class="text-center border-start">Applicants</th>
                        </tr>
                        <tr>
                            <th></th>
                            <th>Job title</th>
                            <th>Status</th>
                            <th class="text-center border-start">Invited</th>
                            <th class="text-center">Applied</th>
                            <th class="text-center">Selected</th>
                            <th class="text-center">Declined</th>
                        </tr>
                    </thead>
                    <tbody>
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
                            <td><a :href="`/job-posting/${job.id}/`">{{job.jobTitle}}</a></td>
                            <td>{{getJobStatus(job)}}</td>
                            <td class="text-center border-start">{{job.applications.filter((a) => !Boolean(a.submissionDateTime)).length}}</td>
                            <td class="text-center">{{job.applications.filter((a) => Boolean(a.submissionDateTime)).length}}</td>
                            <td class="text-center">{{job.applications.filter((a) => Boolean(a.approveDateTime)).length}}</td>
                            <td class="text-center">{{job.applications.filter((a) => Boolean(a.declineDateTime)).length}}</td>
                        </tr>
                        <tr v-if="!initData.employer.jobs.length">
                            <td colspan="7">Post your first job</td>
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
                            <th>Name</th>
                            <th>Status</th>
                            <th>Job Title</th>
                            <th>Project</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="application in applications" class="hover-menu">
                            <td>
                                <HamburgerDropdown :elId="getNewElUid()">
                                    <li>
                                        <a class="dropdown-item" href="#"><i class="far fa-envelope"></i> Message</a>
                                    </li>
                                    <li
                                        v-if="getApplicationStatus(application) !== APPLICATION_STATUS.NOT_SUBMITTED"
                                        @click="eventBus.emit('open:viewCandidateApplicationModal', application.userProject)"
                                    >
                                        <a class="dropdown-item" href="#">
                                            <i class="far fa-eye"></i> Quick view application
                                        </a>
                                    </li>
                                    <li @click="approveApplication(application)">
                                        <a class="dropdown-item" href="#">
                                            <i class="far fa-thumbs-up"></i> Approve <InfoToolTip :elId="getNewElUid()" :content="TOOLTIPS.employerApprove"/>
                                        </a>
                                    </li>
                                    <li @click="declineApplication(application)">
                                        <a class="dropdown-item" href="#">
                                            <i class="far fa-thumbs-down"></i> Decline <InfoToolTip :elId="getNewElUid()" :content="TOOLTIPS.employerDecline"/>
                                        </a>
                                    </li>
                                </HamburgerDropdown>
                            </td>
                            <td>{{application.userProject.user.firstName}} {{application.userProject.user.lastName}}</td>
                            <td>{{getApplicationStatus(application)}}</td>
                            <td>{{application.job.jobTitle}}</td>
                            <td>{{application.userProject.customProject.projectTitle}}</td>
                        </tr>
                        <tr v-if="!applications.length">
                            <td colspan="5">No job applications</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="col-md-9 card-custom table-responsive-md">
                <h3>Linked projects</h3>
                <table class="table mt-3">
                    <thead>
                        <tr>
                            <th></th>
                            <th>Project</th>
                            <th>Career level</th>
                            <th>Skills</th>
                            <th>Linked jobs</th>
                        </tr>
                    </thead>
                    <tbody>
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
                        <tr v-if="!Object.keys(customProjects).length">
                            <td colspan="5"><a href="/projects/">Find a project to get started</a></td>
                        </tr>
                    </tbody>
                </table>
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
        <EditCustomProjectModal/>
        <EditEmployerModal/>
        <EditJobPostingModal/>
        <InviteJobApplicantModal/>
        <ViewCandidateApplicationModal/>
    </div>
</template>

<script>
import {dateSerializer} from "../../../utils/dateUtil";
import dataUtil, {APPLICATION_STATUS} from "../../../utils/data";
import dayjs from "dayjs/esm";
import BadgesSkillLevels from "../../components/BadgesSkillLevels";
import BadgesSkills from "../../components/BadgesSkills";
import BannerAlert from "../../components/BannerAlert";
import EditCustomProjectModal from "../../modals/EditCustomProjectModal";
import EditEmployerModal from "../../modals/EditEmployerModal";
import EditJobPostingModal from "../../modals/EditJobPostingModal";
import HamburgerDropdown from "../../components/HamburgerDropdown";
import InfoToolTip from "../../components/InfoToolTip";
import InviteJobApplicantModal from "../../modals/InviteJobApplicantModal";
import ViewCandidateApplicationModal from "../../modals/ViewCandidateApplicationModal";

export default {
    name: "EmployerDashboardPage.vue",
    components: {
        BannerAlert, BadgesSkillLevels, BadgesSkills, EditCustomProjectModal, EditEmployerModal, EditJobPostingModal,
        HamburgerDropdown, InfoToolTip, InviteJobApplicantModal, ViewCandidateApplicationModal
    },
    data() {
        return {
            APPLICATION_STATUS
        }
    },
    computed: {
        applications() {
            return this.initData.employer.jobs.reduce((applications, job) => {
                return [...applications, ...job.applications.map((app) => {
                    app.job = {
                        id: job.id,
                        jobTitle: job.jobTitle
                    };
                    return app;
                })];
            }, []);
        },
        customProjects() {
            return this.initData.employer.jobs.reduce((customProjects, job) => {
                job.allowedProjects.forEach((ap) => {
                    if (ap.id in customProjects) {
                        customProjects[ap.id].jobs.push({id: job.id, jobTitle: job.jobTitle});
                    } else {
                        ap.jobs = [{id: job.id, jobTitle: job.jobTitle}];
                        ap.skillLevel = dataUtil.getSkillLevelsFromBits(ap.skillLevelBit, this.globalData.SKILL_LEVEL);
                        customProjects[ap.id] = ap;
                    }
                });
                return customProjects;
            }, {});
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
                approveDateTime: dateSerializer.serializeDateTime(dayjs())
            });
            this.submitAjaxRequest(ajaxData, {
                url: this.apiUrl + 'user-job-application/',
                success: (data) => {
                    application.approveDateTime = data.approveDateTime;
                    application.declineDateTime = null;
                }
            });
        },
        declineApplication(application) {
            const ajaxData = this.getAjaxFormData({
                id: application.id,
                declineDateTime: dateSerializer.serializeDateTime(dayjs())
            });
            this.submitAjaxRequest(ajaxData, {
                url: this.apiUrl + 'user-job-application/',
                success: (data) => {
                    application.approveDateTime = null;
                    application.declineDateTime = data.declineDateTime;
                }
            });
        }
    }
}
</script>