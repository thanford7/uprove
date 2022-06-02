<template>
    <BasePage>
        <ul class="nav nav-tabs" id="employerTabs" role="tablist">
            <li class="nav-item" role="presentation">
                <button
                    class="nav-link" id="job-openings-tab"
                    :class="(currentTab === 'job-openings') ? 'active': ''"
                    data-bs-toggle="tab" data-bs-target="#job-openings"
                    type="button" role="tab" aria-selected="true"
                    @click="setTabParam('job-openings')"
                >Job openings
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
                    class="nav-link" id="settings-tab"
                    :class="(currentTab === 'settings') ? 'active': ''"
                    data-bs-toggle="tab" data-bs-target="#settings"
                    type="button" role="tab" aria-selected="false"
                    @click="setTabParam('settings')"
                >Settings
                </button>
            </li>
            <li class="nav-item">
                <button
                    class="nav-link" id="users-tab"
                    :class="(currentTab === 'users') ? 'active': ''"
                    data-bs-toggle="tab" data-bs-target="#users"
                    type="button" role="tab" aria-selected="false"
                    @click="setTabParam('users')"
                >Users
                </button>
            </li>
            <li class="nav-item">
                <button
                    class="nav-link" id="integrations-tab"
                    :class="(currentTab === 'integrations') ? 'active': ''"
                    data-bs-toggle="tab" data-bs-target="#integrations"
                    type="button" role="tab" aria-selected="false"
                    @click="setTabParam('integrations')"
                >Integrations
                </button>
            </li>
        </ul>
        <div class="tab-content mb-3" id="employerTabContent">
            <div class="tab-pane fade" :class="(currentTab === 'job-openings') ? 'show active': ''" id="job-openings" role="tabpanel">
                <div class="mb-2 d-flex justify-content-end">
                    <FilterDropdownMenu class="-pull-left" :filters="jobsFilter" dropdownHeader="Filters">
                        <div class="ps-2 pe-2">
                            <InputSelectize
                                :elId="getNewElUid()"
                                placeholder="Status"
                                :cfg="{
                                    plugins: ['remove_button'],
                                    maxItems: null,
                                    options: Object.values(globalData.JOB_STATUS).map((v) => ({value: v, text: v}))
                                }"
                                @selected="jobsFilter.statuses = $event"
                            />
                        </div>
                    </FilterDropdownMenu>
                    <button type="button" class="btn btn-primary me-2"
                            @click="eventBus.emit('open:editJobPostingModal')">
                        Create job posting
                    </button>
                    <button v-if="initData.employer.isLeverOn" type="button" class="btn btn-secondary"
                            @click="loadLeverJobPostings">
                        Pull from Lever
                        <InfoToolTip :elId="getNewElUid()" content="Any job postings with the 'uprove' tag will be created
                        and/or updated in Uprove.
                        "/>
                    </button>
                </div>
                <div class="table-responsive-md">
                    <Table
                        :data="initData.employer.jobs"
                        :headers="[
                            [{colspan: 3}, {value: 'Applicants', colspan: 4, classes: 'text-center border-start'}],
                            [
                                {},
                                {value: 'Job title', sortFn: 'jobTitle'},
                                {value: 'Status', sortFn: getJobStatus},
                                {value: 'Invited', classes: 'text-center border-start'},
                                {value: 'Applied', classes: 'text-center'},
                                {value: 'Approved', classes: 'text-center'},
                                {value: 'Declined', classes: 'text-center'}
                            ]
                        ]"
                        emptyDataMessage="Post your first job"
                    >
                        <template v-slot:body>
                            <tr v-for="job in filteredJobs" class="hover-menu">
                                <td>
                                    <HamburgerDropdown :elId="getNewElUid()">
                                        <li>
                                            <a class="dropdown-item" href="#"
                                               @click="eventBus.emit('open:editJobPostingModal', job)">
                                                <i class="fas fa-pencil-alt"></i> Edit job
                                            </a>
                                        </li>
                                        <li>
                                            <a class="dropdown-item" href="#"
                                               @click="eventBus.emit('open:inviteJobApplicantModal', job)">
                                                <i class="fas fa-user-plus"></i> Invite applicants
                                            </a>
                                        </li>
                                    </HamburgerDropdown>
                                </td>
                                <td title="View job posting">
                                    <InfoToolTip
                                        v-if="!job.roleId"
                                        :elId="getNewElUid()"
                                        content="This job does not have a standardized role and will not show up in job searches"
                                        :isExcludeInfoCircle="true"
                                    >
                                        <i class="fas fa-exclamation-triangle -color-orange-text"></i>&nbsp;
                                    </InfoToolTip>
                                    <a :href="`/job-posting/${job.id}/`">{{ job.jobTitle }}</a>
                                </td>
                                <td>{{ getJobStatus(job) }}</td>
                                <td class="text-center border-start">
                                    {{ job.applications.filter((a) => !Boolean(a.submissionDateTime)).length }}
                                </td>
                                <td class="text-center">
                                    {{ job.applications.filter((a) => Boolean(a.submissionDateTime)).length }}
                                </td>
                                <td class="text-center">
                                    {{ job.applications.filter((a) => Boolean(a.approveDateTime)).length }}
                                </td>
                                <td class="text-center">
                                    {{ job.applications.filter((a) => Boolean(a.declineDateTime)).length }}
                                </td>
                            </tr>
                        </template>
                    </Table>
                </div>
            </div>
            <div class="tab-pane fade" :class="(currentTab === 'applications') ? 'show active': ''" id="applications" role="tabpanel">
                <div class="mb-2">
                    <FilterDropdownMenu class="-pull-left" :filters="applicantsFilter" dropdownHeader="Filters">
                        <div class="ps-2 pe-2">
                            <InputSelectize
                                :elId="getNewElUid()"
                                placeholder="Status"
                                :cfg="{
                                    plugins: ['remove_button'],
                                    maxItems: null,
                                    options: Object.values(APPLICATION_STATUS).map((v) => ({value: v, text: v}))
                                }"
                                @selected="applicantsFilter.statuses = $event"
                            />
                            <InputSelectize
                                ref="jobTitleFilter"
                                :elId="getNewElUid()"
                                placeholder="Job title"
                                :cfg="{
                                    plugins: ['remove_button'],
                                    maxItems: null,
                                    sortField: 'text'
                                }"
                                @selected="applicantsFilter.jobTitle = $event"
                            />
                        </div>
                    </FilterDropdownMenu>
                </div>
                <div class="table-responsive-md">
                    <Table
                        class="mt-3"
                        :data="applications"
                        :headers="[
                                [
                                    {},
                                    {value: 'Name', sortFn: 'user.firstName'},
                                    {value: 'Status', sortFn: getApplicationStatus},
                                    {value: 'Job title', sortFn: 'job.jobTitle'},
                                ]
                            ]"
                        emptyDataMessage="No job applications"
                    >
                        <template v-slot:body>
                            <tr v-for="application in filteredApplications" class="hover-menu">
                                <td>
                                    <ApplicationDropdownOpts :application="application" :applications="applications"/>
                                </td>
                                <td>
                                    <a
                                        :href="`/profile/${application.user.profileId}/`"
                                        :title="`${application.user.firstName} ${application.user.lastName}'s Profile`"
                                        target="_blank"
                                    >
                                        {{ application.user.firstName }} {{ application.user.lastName }}
                                    </a>
                                </td>
                                <td>{{ getApplicationStatusText(application) }}</td>
                                <td>{{ application.job.jobTitle }}</td>
                            </tr>
                        </template>
                    </Table>
                </div>
            </div>
            <div class="tab-pane fade" :class="(currentTab === 'settings') ? 'show active': ''" id="settings" role="tabpanel">
                <div>
                    <a href="#" @click="eventBus.emit('open:editEmployerModal', initData.employer)">Edit employer
                        information</a>
                </div>
                <!--                    <a href="#">Manage users</a>-->
                <!--                    <a href="#">Update billing</a>-->
            </div>
            <div class="tab-pane fade" :class="(currentTab === 'users') ? 'show active': ''" id="users" role="tabpanel">
                <div class="mb-2 d-flex justify-content-end">
                    <button v-if="initData.employer.isLeverOn" type="button" class="btn btn-secondary"
                            @click="connectLeverUsers">
                        Connect to Lever
                        <InfoToolTip :elId="getNewElUid()" content="Connect all current users with Lever so they can push
                        candidates directly to Lever."/>
                    </button>
                </div>
                <div class="table-responsive-md">
                    <Table
                        class="mt-3"
                        :data="initData.users"
                        :headers="userTableHeaders"
                        emptyDataMessage="<a href='/projects/'>No current users</a>"
                    >
                        <template v-slot:body>
                            <tr v-for="user in initData.users" class="hover-menu">
                                <td>
                                    <HamburgerDropdown :elId="getNewElUid()">
                                        <li @click="eventBus.emit('open:editUserModal', user)">
                                            <a class="dropdown-item" href="#"><i class="fas fa-pencil-alt"></i> Edit
                                                user</a>
                                        </li>
                                    </HamburgerDropdown>
                                </td>
                                <td>{{ user.firstName }}</td>
                                <td>{{ user.lastName }}</td>
                                <td>{{ user.email }}</td>
                                <td v-if="initData.employer.isLeverOn">
                                    <i v-if="user.leverUserKey" class="fas fa-check-circle -color-green-text"></i>
                                    <i v-else class="fas fa-times-circle -color-red-text"></i>
                                </td>
                            </tr>
                        </template>
                    </Table>
                </div>
            </div>
            <div class="tab-pane fade" :class="(currentTab === 'integrations') ? 'show active': ''" id="integrations" role="tabpanel">
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
                        <div class="-text-medium mb-3">
                            Webhooks allow us to automatically update candidate information and send Uprove assessments
                            to candidates based on changes in Lever. This means less clicks for you! To enable webhooks,
                            a Lever user with "Super Admin" privileges must go to <code>Settings
                            ->
                            Integrations and API -> Webhooks</code> and toggle on the webhooks for:
                            <ul>
                                <li>Candidate stage change</li>
                                <li>Candidate archive state change</li>
                                <li>Candidate hired</li>
                                <li>Candidate deleted</li>
                            </ul>
                            <div class="mt-2">
                                A <span class="badge -color-moderategrey">uprove</span> tag must be added to all job
                                postings
                                and candidates that should receive a Uprove assessment. If the tag is added to a job
                                posting,
                                all candidates assigned to that job posting will automatically inherit that tag.
                            </div>
                        </div>
                        <div class="col-md-6">
                            <span id="leverStageLabel" class="-text-medium">
                                Stage to send Uprove assessment
                                <InfoToolTip :elId="getNewElUid()" content="
                                When a candidate is moved to this stage and has the 'uprove' tag, a link will be
                                generated in the candidate's links which will allow you to select and send an
                                assessment to the candidate.
                                "/>
                            </span>
                            <InputSelectize
                                ref="leverStage"
                                :elId="getNewElUid()"
                                placeholder="Required"
                                :cfg="{
                                    valueField: 'id',
                                    labelField: 'text',
                                    searchField: 'text',
                                    maxItems: 1
                                }"
                                @selected="saveToken($event, 'leverTriggerStageKey', '#leverStageLabel')"
                            />
                        </div>
                        <div class="col-md-6">
                            <span id="leverStageCompleteLabel" class="-text-medium">
                                Stage after assessment complete
                                <InfoToolTip :elId="getNewElUid()" content="
                                When a candidate has completed an assessment they will automatically be moved to this
                                stage in Lever.
                                "/>
                            </span>
                            <InputSelectize
                                ref="leverStageComplete"
                                :elId="getNewElUid()"
                                placeholder="Optional"
                                :cfg="{
                                    valueField: 'id',
                                    labelField: 'text',
                                    searchField: 'text',
                                    maxItems: 1
                                }"
                                @selected="saveToken($event, 'leverCompleteStageKey', '#leverStageCompleteLabel')"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </BasePage>
    <CelebrationModal/>
    <EditEmployerModal/>
    <EditJobPostingModal/>
    <EditUserModal/>
    <InviteJobApplicantModal/>
</template>

<script>
import dataUtil, {APPLICATION_STATUS} from "../../../utils/data";
import ApplicationDropdownOpts from "./ApplicationDropdownOpts";
import BadgesSkillLevels from "../../components/BadgesSkillLevels";
import BadgesSkills from "../../components/BadgesSkills";
import BannerAlert from "../../components/BannerAlert";
import BasePage from "../base/BasePage";
import CelebrationModal from "../../modals/CelebrationModal";
import EditEmployerModal from "../../modals/EditEmployerModal";
import EditJobPostingModal from "../../modals/EditJobPostingModal";
import EditUserModal from "../../modals/EditUserModal";
import FilterDropdownMenu from "../../components/FilterDropdownMenu";
import HamburgerDropdown from "../../components/HamburgerDropdown";
import InfoToolTip from "../../components/InfoToolTip";
import InputSelectize from "../../inputs/InputSelectize";
import InviteJobApplicantModal from "../../modals/InviteJobApplicantModal";
import leverIntegration from "../../../utils/leverIntegration";
import RangeSlider from "../../components/RangeSlider";
import Table from "../../components/Table";
import LeverWebhook from "./LeverWebhook";
import userProject from "../../../utils/userProject";
import RolesSelectize from "../../inputs/RolesSelectize";

export default {
    name: "EmployerDashboardPage.vue",
    components: {
        ApplicationDropdownOpts, BannerAlert, BadgesSkillLevels, BadgesSkills, BasePage, CelebrationModal, EditEmployerModal,
        EditJobPostingModal, EditUserModal, FilterDropdownMenu, HamburgerDropdown, InfoToolTip, InputSelectize,
        InviteJobApplicantModal, LeverWebhook, RangeSlider, RolesSelectize, Table
    },
    data() {
        return {
            APPLICATION_STATUS,
            applications: [],
            sortKeysJobPostingTable: [],
            leverData: {},
            leverWebhookTypes: leverIntegration.TYPES,
            jobsFilter: {},
            applicantsFilter: {}
        }
    },
    computed: {
        filteredApplications() {
            return this.applications.filter((application) => {
                if (this.applicantsFilter?.statuses?.length && !this.applicantsFilter.statuses.includes(this.getApplicationStatus(application))) {
                    return false;
                }

                if (this.applicantsFilter?.jobTitle?.length && !this.applicantsFilter.jobTitle.includes(application.job.jobTitle)) {
                    return false;
                }

                return true;
            });
        },
        filteredJobs() {
            return this.initData.employer.jobs.filter((job) => {
                if (this.jobsFilter?.statuses?.length && !this.jobsFilter.statuses.includes(this.getJobStatus(job))) {
                    return false;
                }

                return true;
            });
        },
        userTableHeaders() {
            const baseHeaders = [
                    {},
                    {value: 'First name', sortFn: 'firstName'},
                    {value: 'Last name', sortFn: 'lastName'},
                    {value: 'Email', sortFn: 'email'},
            ];

            if (this.initData.employer.isLeverOn) {
                baseHeaders.push({
                    value: 'Has Lever connection',
                    toolTip: 'Each user needs to be connected with Lever to be able to push candidates directly to Lever. Use the "Connect to Lever" button to create the connection for users that have a Lever account.'
                });
            }

            return [baseHeaders];
        }
    },
    methods: {
        declineApplication: userProject.declineApplication.bind(userProject),
        approveApplication: userProject.approveApplication.bind(userProject),
        getApplicationStatus: dataUtil.getApplicationStatus.bind(dataUtil),
        getApplicationStatusText: dataUtil.getApplicationStatusText.bind(dataUtil),
        leverLogin: function (isOn) {
            if (isOn) {
                leverIntegration.login();
            } else {
                leverIntegration.logout(this.initData.employer.id, () => {
                    this.leverData.isLeverOn = false;
                });
            }
        },
        saveToken(val, modelName, targetEl) {
            leverIntegration.saveToken($(targetEl), this.initData.employer.id, modelName, val)
        },
        loadLeverJobPostings() {
            leverIntegration.loadJobPostings(this.initData.employer.id);
        },
        connectLeverUsers() {
            leverIntegration.connectUsers(this.initData.employer.id)
        },
        getJobStatus(job) {
            if (job.closeDate) {
                return this.globalData.JOB_STATUS.CLOSED;
            }
            if (job.pauseDate) {
                return this.globalData.JOB_STATUS.PAUSED;
            }
            if (job.openDate) {
                return this.globalData.JOB_STATUS.OPEN;
            }
            return this.globalData.JOB_STATUS.DRAFT;
        },
    },
    async mounted() {
        this.applications = this.initData.employer.jobs.reduce((applications, job) => {
            return [...applications, ...job.applications.map((app) => {
                app.job = {
                    id: job.id,
                    jobTitle: job.jobTitle
                };
                return app;
            })];
        }, []);

        const jobTitles = dataUtil.uniqArray(this.applications.map((a) => a.job.jobTitle));
        this.$refs.jobTitleFilter.resetOptions(jobTitles.map((v) => ({value: v, text: v})));

        this.currentTab = 'job-openings';
        this.setTabFromParams();

        this.leverData = dataUtil.pick(this.initData.employer, [
            'isLeverOn', 'leverHookStageChangeToken', 'leverHookArchive', 'leverHookHired', 'leverHookDeleted'
        ]);
        if (this.leverData.isLeverOn) {
            await this.loadData([{route: `lever/stages/${this.initData.employer.id}/`, dataKey: 'leverStages'}]);
            this.$refs.leverStage.resetOptions(this.cData.leverStages);
            this.$refs.leverStage.elSel.setValue(this.initData.employer.leverTriggerStageKey, true);
            this.$refs.leverStageComplete.resetOptions(this.cData.leverStages);
            this.$refs.leverStageComplete.elSel.setValue(this.initData.employer.leverCompleteStageKey, true);
        }
    }
}
</script>