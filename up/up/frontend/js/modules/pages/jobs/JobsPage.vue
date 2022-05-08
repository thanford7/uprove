<template>
    <BasePage>
        <template v-slot:filter>
            <BaseFilter>
                <div class="col-12 d-flex justify-content-between mb-3">
                    <h6 style="display: inline-block;">Search jobs</h6>
                    <div
                        class="btn btn-sm btn-secondary ms-2"
                        @click="eventBus.emit('open:editJobPreferencesModal', initData.preferences)"
                    >
                        <i class="fas fa-sliders-h"></i> Update job preferences
                    </div>
                </div>
                <div class="row">
                    <div class="col-12 col-md-3 filter-item">
                        <InputSelectize
                            ref="roles"
                            :elId="getNewElUid()"
                            :cfg="roleCfg"
                            :isParseAsInt="true"
                            :isPreserveValue="true"
                            placeholder="All roles"
                            @selected="updateFilters($event, 'roles')"
                        />
                    </div>
                    <div class="col-12 col-md-3 filter-item">
                        <InputSelectize
                            ref="countries"
                            :elId="getNewElUid()"
                            :cfg="countryCfg"
                            :isParseAsInt="true"
                            :isPreserveValue="true"
                            placeholder="All countries"
                            @selected="updateFilters($event, 'countries')"
                        />
                    </div>
                    <div class="col-12 col-md-3 filter-item">
                        <InputSelectize
                            ref="states"
                            :elId="getNewElUid()"
                            :cfg="stateCfg"
                            :isParseAsInt="true"
                            :isPreserveValue="true"
                            placeholder="All states"
                            @selected="updateFilters($event, 'states')"
                        />
                    </div>
                    <div class="col-12 col-md-3 filter-item">
                        <InputSelectize
                            ref="companySize"
                            :elId="getNewElUid()"
                            :cfg="companySizeCfg"
                            :isParseAsInt="true"
                            :isPreserveValue="true"
                            placeholder="All sizes"
                            @selected="updateFilters($event, 'companySizes')"
                        />
                    </div>
                    <div class="col-12 col-md-3 filter-item">
                        <InputSelectize
                            ref="employers"
                            :elId="getNewElUid()"
                            :cfg="employerCfg"
                            :isParseAsInt="true"
                            :isPreserveValue="true"
                            placeholder="All employers"
                            @selected="updateFilters($event, 'employers')"
                        />
                    </div>
                    <div class="col-12 col-md-3 filter-item d-flex align-items-center">
                        <InputCheckBox
                            label="Remote work"
                            @click="updateFilters($event, 'isRemote')"
                            :isChecked="getQueryParams().isRemote === 'true'"
                        />
                    </div>
                </div>
            </BaseFilter>
        </template>
        <div class="jobs row mb-4">
            <div class="p-0" :class="(selectedJob) ? 'col-md-6' : 'col-md-12'">
                <div v-for="job in pageJobs" class="card-custom card-custom--no-side-margin">
                    <div class="row mb-2">
                        <div class="job-role -color-darkblue -color-white-text">
                            <UprovePartner v-if="job.isClient"/>
                            {{ job.roleName }}
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-2 d-flex align-items-center justify-content-center">
                            <img v-if="job.employerLogo" :src="job.employerLogo"
                                 class="logo">
                            <i v-else class="far fa-building fa-4x"></i>
                        </div>
                        <div class="col-md-7">
                            <a href="#" @click="showJobDetails($event, job)"><h5>{{ job.jobTitle }}</h5></a>
                            <h6>{{ getEmployer(job.employerId).companyName }}</h6>
                            <h6>{{ getLocationStr(job) }}</h6>
                        </div>
                        <div v-if="!selectedJob" class="col-md-3 -border-left--light -text-medium">
                            <JobHelpLinks :job="job" :employer="getEmployer(job.employerId)"/>
                        </div>
                    </div>
                </div>
            </div>
            <div v-if="selectedJob" id="selectedJob" class="col-md-6" style="padding-top: 20px;">
                <JobPosting
                    ref="jobPosting"
                    class="-text-medium sticky-md-top"
                    :employer="getEmployer(selectedJob.employerId)"
                    :job="selectedJob"
                    :isJobDescriptionOpen="true"
                >
                    <template v-slot:top>
                        <AccordionItem :accordionElId="$refs.jobPosting.accordionElId" :elId="getNewElUid()"
                                       :isOpen="true">
                            <template v-slot:header>
                                Overview
                            </template>
                            <template v-slot:body>
                                <div class="row">
                                    <div class="col-9">
                                        <h5>{{ selectedJob.jobTitle }}</h5>
                                        <h6>{{ getEmployer(selectedJob.employerId).companyName }} |
                                            {{ getLocationStr(selectedJob) }}</h6>
                                    </div>
                                    <div class="col-3">
                                        <JobApplyBtn :applicationUrl="selectedJob.applicationUrl"/>
                                    </div>
                                </div>
                                <JobHelpLinks :job="selectedJob" :employer="getEmployer(selectedJob.employerId)"/>
                            </template>
                        </AccordionItem>
                    </template>
                </JobPosting>
            </div>
            <Pagination
                ref="jobsPagination"
                :items="jobs"
                :itemsPerPage="jobsPerPage"
                class="ms-1"
                @pageChange="jobPaginationIdx = ($event - 1) * jobsPerPage"
            />
        </div>
    </BasePage>
    <EditJobPreferencesModal :isResetUrl="true"/>
</template>

<script>
import {REMOTE_BITS, SEVERITY} from '../../../globalData';
import AccordionItem from "../../components/AccordionItem";
import BaseFilter from "../base/BaseFilter";
import BasePage from "../base/BasePage";
import dataUtil from "../../../utils/data";
import EditJobPreferencesModal from "../../modals/EditJobPreferencesModal";
import InputCheckBox from "../../inputs/InputCheckBox";
import InputSelectize from "../../inputs/InputSelectize";
import JobApplyBtn from "./JobApplyBtn";
import JobPosting from "../jobPosting/JobPosting";
import Pagination from "../../components/Pagination";
import ListFontAwesome from "../../components/ListFontAwesome";
import JobHelpLinks from "./JobHelpLinks";
import jobUtil from "../../../utils/jobs";
import UprovePartner from "./UprovePartner";

export default {
    name: "JobsPage",
    components: {
        AccordionItem, BaseFilter, BasePage, EditJobPreferencesModal, InputCheckBox,
        InputSelectize, JobApplyBtn, JobHelpLinks, JobPosting, ListFontAwesome, Pagination, UprovePartner
    },
    data() {
        return {
            filter: {
                roles: [],
                countries: [],
                states: [],
                employers: [],
                isRemote: null
            },
            jobPaginationIdx: 0,
            jobsPerPage: 25,
            selectedJob: null,
        }
    },
    computed: {
        roleCfg() {
            return {
                valueField: 'id',
                labelField: 'roleTitle',
                sortField: 'roleTitle',
                maxItems: null,
                plugins: ['remove_button'],
                options: this.initData.roleLevels
            };
        },
        companySizeCfg() {
            return {
                valueField: 'id',
                labelField: 'companySize',
                sortField: 'id',
                maxItems: null,
                plugins: ['remove_button'],
                options: this.initData.companySizes
            };
        },
        countryCfg() {
            return {
                valueField: 'id',
                labelField: 'countryName',
                sortField: 'countryName',
                maxItems: null,
                plugins: ['remove_button'],
                options: this.initData.countries
            };
        },
        employerCfg() {
            return {
                valueField: 'id',
                labelField: 'companyName',
                sortField: 'companyName',
                maxItems: null,
                plugins: ['remove_button'],
                options: Object.values(this.initData.employers)
            };
        },
        stateCfg() {
            return {
                valueField: 'id',
                labelField: 'stateName',
                sortField: 'stateName',
                maxItems: null,
                plugins: ['remove_button'],
                options: this.initData.states
            };
        },
        jobs() {
            return this.initData.jobs.filter((j) => {
                if (this.filter.roles?.length && !this.filter.roles.includes(j.roleLevelId)) {
                    return false;
                }
                if (this.filter.countries?.length && !this.filter.countries.includes(j.countryId)) {
                    return false;
                }
                if (this.filter.states?.length && !this.filter.states.includes(j.stateId)) {
                    return false;
                }
                if (this.filter.employers?.length && !this.filter.employers.includes(j.employerId)) {
                    return false;
                }
                if (this.filter.companySizes?.length && !this.filter.companySizes.includes(j.companySizeId)) {
                    return false;
                }
                if (this.filter.isRemote && !j.isRemote) {
                    return false;
                }
                return true;
            });
        },
        pageJobs() {
            return this.jobs.slice(this.jobPaginationIdx, this.jobPaginationIdx + this.jobsPerPage + 1);
        },
    },
    methods: {
        getQueryParams: dataUtil.getQueryParams,
        getLocationStr: jobUtil.getLocationStr,
        getEmployer(employerId) {
            return this.initData['employers'][employerId];
        },
        showJobDetails(e, job) {
            e.preventDefault();
            this.selectedJob = job;

        },
        updateFilters(val, filterKey) {
            this.setFilter(val, filterKey);

            // Update the available options based on other filters
            const options = {roles: new Set(), countries: new Set(), employers: new Set(), states: new Set()};
            this.jobs.forEach((job) => {
                if (job.roleId) {
                    options.roles.add(this.initData.roleLevels.find((r) => r.id === job.roleLevelId));
                }
                if (job.stateId) {
                    options.states.add(this.initData.states.find((s) => s.id === job.stateId));
                }
                if (job.countryId) {
                    options.countries.add(this.initData.countries.find((c) => c.id === job.countryId));
                }
                options.employers.add(this.initData.employers[job.employerId])
            });
            ['roles', 'countries', 'employers', 'states'].forEach((ref) => {
                // Don't update options for the current selectize. Otherwise all other options will be removed.
                if (ref === filterKey && val && val.length) {
                    return;
                }
                const sel = this.$refs[ref];
                if (sel) {
                    sel.resetOptions(Array.from(options[ref]));
                }
            });

            const pagination = this.$refs.jobsPagination;
            if (pagination) {
                pagination.reset(); // Reset page counts
            }
        },
        hasUserPreferences() {
            return Object.values(this.initData.preferences).reduce((hasPreference, p) => {
                hasPreference = hasPreference || ((Array.isArray(p)) ? p.length : Boolean(p));
                return hasPreference;
            }, false);
        }
    },
    mounted() {
        let queryParams = dataUtil.getQueryParams();
        if (dataUtil.isEmpty(queryParams) && this.hasUserPreferences()) {
            // Extract the ids from each preference
            queryParams = Object.entries(this.initData.preferences).reduce((flattenedParams, [key, val]) => {
                flattenedParams[key] = dataUtil.flattenObjects(val, 'id');
                return flattenedParams;
            }, {});
            this.addPopover($('.filter'),
                {severity: SEVERITY.INFO, content: 'Filters set based on the your default job preferences', isOnce: true}
            );
        }
        this.$refs.roles.elSel.setValue(queryParams.roles);
        this.$refs.states.elSel.setValue(queryParams.states);
        this.$refs.countries.elSel.setValue(queryParams.countries);
        this.$refs.employers.elSel.setValue(queryParams.employers);
        this.$refs.companySize.elSel.setValue(queryParams.companySizes);
        this.filter.isRemote = queryParams.isRemote === 'true' || queryParams.remoteBits === REMOTE_BITS.REMOTE;
    }
}
</script>