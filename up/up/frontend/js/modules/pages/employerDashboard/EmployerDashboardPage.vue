<template>
    <BasePage>
        <ul class="nav nav-tabs" id="employerTabs" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active" id="job-openings-tab" data-bs-toggle="tab" data-bs-target="#job-openings" type="button" role="tab" aria-selected="true">Job openings</button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="applications-tab" data-bs-toggle="tab" data-bs-target="#applications" type="button" role="tab" aria-selected="false">Applications</button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="projects-tab" data-bs-toggle="tab" data-bs-target="#projects" type="button" role="tab" aria-selected="false">Projects</button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="settings-tab" data-bs-toggle="tab" data-bs-target="#settings" type="button" role="tab" aria-selected="false">Settings</button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="integrations-tab" data-bs-toggle="tab" data-bs-target="#integrations" type="button" role="tab" aria-selected="false">Integrations</button>
            </li>
        </ul>
        <div class="tab-content" id="employerTabContent">
            <div class="tab-pane fade show active" id="job-openings" role="tabpanel">
                <div class="table-responsive-md">
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
            </div>
            <div class="tab-pane fade" id="applications" role="tabpanel">
                <div class="table-responsive-md">
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
                                    {value: 'Project score', sortFn: 'userProject.evaluationScorePct'}
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
                                                @click="eventBus.emit('open:viewCandidateApplicationModal', {application})"
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
                                    <td>{{(application?.userProject?.evaluationScorePct) ? `${application?.userProject?.evaluationScorePct}%` : 'None'}}</td>
                                </tr>
                            </template>
                        </Table>
                    </div>
            </div>
            <div class="tab-pane fade" id="projects" role="tabpanel">
                <div class="table-responsive-md">
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
            </div>
            <div class="tab-pane fade" id="settings" role="tabpanel">
                    <div>
                        <a href="#" @click="eventBus.emit('open:editEmployerModal', initData.employer)">Edit employer information</a>
                    </div>
<!--                    <a href="#">Manage users</a>-->
<!--                    <a href="#">Update billing</a>-->
            </div>
            <div class="tab-pane fade" id="integrations" role="tabpanel">
                <div class="card-custom">
                    <div class="d-flex align-items-center">
                        <div class="btn-group" role="group">
                            <button
                                type="button" class="btn"
                                :class="(leverData.isLeverOn) ? 'btn-success' : 'btn-outline-success'"
                                @click="leverLogin(true)"
                            >
                                On
                            </button>
                            <button
                                type="button" class="btn"
                                :class="(!leverData.isLeverOn) ? 'btn-danger' : 'btn-outline-danger'"
                                @click="leverLogin(false)"
                            >
                                Off
                            </button>
                        </div>
                        <img class="line-height ms-3" :src="globalData.STATIC_URL + 'img/leverLogo.png'">
                        Lever
                    </div>
                    <div class="-text-medium mt-3">
                        Integrate with Lever to automatically send candidates a Uprove assessment based on a
                        specified stage change. The integration also allows you to add candidates from Uprove
                        into your Lever opportunities with a single button click.
                    </div>
                    <div v-if="leverData.isLeverOn" class="row mt-3">
                        <h5>Webhooks</h5>
                        <div class="-text-medium">
                            Webhooks allow us to automatically update candidate information and send Uprove assessments
                            to candidates based on changes in Lever. This means less clicks for you! Go to <code>Settings ->
                            Integrations and API -> Webhooks</code> to get and set the necessary fields described below. For
                            each webhook:
                            <ul class="mt-2">
                                <li>Click the toggle button next to the webhook in Lever to turn it on</li>
                                <li>Click the "Add webhook" button</li>
                                <li>Copy the signature token from Lever and paste it into the form field for the
                                    corresponding webhook in Uprove
                                </li>
                                <li>Copy the webhook URL from Uprove and paste it into the URL field for the corresponding
                                    webhook in Lever (it's a gray box that begins with "https://")
                                </li>
                                <li>Click the "Verify connection" button in Lever to confirm the webhook is working properly</li>
                            </ul>
                        </div>
                        <LeverWebhook
                            hookName="Candidate Stage Change"
                            hookInfo="
                                This webhook automatically notifies Uprove when a candidate is moved to another stage
                                of the hiring process. When the candidate is moved to the specified stage for the
                                Uprove assessment, they will receive an email from us to initiate the assessment.
                            "
                            :hookType="leverWebhookTypes.stageChange"
                            :employer="initData.employer"
                            :leverData="leverData"
                            modelName="leverHookStageChangeToken"
                        />
                        <LeverWebhook
                            hookName="Candidate Archive State Change"
                            hookInfo="
                                This webhook automatically notifies Uprove when a candidate is archived. When this event
                                occurs, all of the candidate's applications will be archived in Uprove.
                            "
                            :hookType="leverWebhookTypes.archive"
                            :employer="initData.employer"
                            :leverData="leverData"
                        />
                        <LeverWebhook
                            hookName="Candidate Hired"
                            hookInfo="
                                This webhook automatically notifies Uprove when a candidate is hired. When this event
                                occurs, the candidate's employment status is updated in Uprove.
                            "
                            :hookType="leverWebhookTypes.hire"
                            :employer="initData.employer"
                            :leverData="leverData"
                        />
                        <LeverWebhook
                            hookName="Candidate Deleted"
                            hookInfo="
                                This webhook automatically notifies Uprove when a candidate is deleted. When this event
                                occurs, all of the candidate's applications will be archived in Uprove.
                            "
                            :hookType="leverWebhookTypes.delete"
                            :employer="initData.employer"
                            :leverData="leverData"
                        />
                    </div>
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
import BasePage from "../base/BasePage";
import EditCustomProjectModal from "../../modals/EditCustomProjectModal";
import EditEmployerModal from "../../modals/EditEmployerModal";
import EditJobPostingModal from "../../modals/EditJobPostingModal";
import HamburgerDropdown from "../../components/HamburgerDropdown";
import InfoToolTip from "../../components/InfoToolTip";
import InviteJobApplicantModal from "../../modals/InviteJobApplicantModal";
import leverIntegration from "../../../utils/leverIntegration";
import Table from "../../components/Table";
import userProjectUtil from "../../../utils/userProject";
import ViewCandidateApplicationModal from "../../modals/ViewCandidateApplicationModal";
import LeverWebhook from "./LeverWebhook";

export default {
    name: "EmployerDashboardPage.vue",
    components: {
        LeverWebhook,
        BannerAlert, BadgesSkillLevels, BadgesSkills, BasePage, EditCustomProjectModal, EditEmployerModal,
        EditJobPostingModal, HamburgerDropdown, InfoToolTip, InviteJobApplicantModal,
        Table, ViewCandidateApplicationModal
    },
    data() {
        return {
            APPLICATION_STATUS,
            applications: null,
            customProjects: null,
            sortKeysJobPostingTable: [],
            leverData: {},
            leverWebhookTypes: leverIntegration.TYPES
        }
    },
    computed: {
        applications() {
            return this.initData.employer.jobs.reduce((applications, job) => {
                return [...applications, ...job.applications.map((app) => {
                    if (app.userProject) {
                        app.userProject.evaluationScorePct = userProjectUtil.getEvaluationScore(app.userProject.evaluationCriteria);
                    }
                    app.job = {
                        id: job.id,
                        jobTitle: job.jobTitle
                    };
                    return app;
                })];
            }, []);
        },
        customProjects() {
            const customProjects = this.initData.employer.jobs.reduce((customProjects, job) => {
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
            return Object.values(customProjects);
        }
    },
    methods: {
        getApplicationStatus: dataUtil.getApplicationStatus,
        leverLogin: (isOn) => {
            if (isOn) {
                leverIntegration.login();
            } else {
                leverIntegration.logout(() => {
                    this.initData.employer.isLeverOn = false;
                });
            }
        },
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
        this.leverData = dataUtil.pick(this.initData.employer, [
            'isLeverOn', 'leverHookStageChangeToken', 'leverHookArchive', 'leverHookHired', 'leverHookDeleted'
        ]);
    }
}
</script>