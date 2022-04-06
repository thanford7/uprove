<template>
    <BasePage>
        <template v-slot:filter>
            <BaseFilter>
                <div class="col-12">
                    <h6>Search jobs</h6>
                </div>
                <div class="row">
                    <div class="col-12 col-md filter-item">
                        <InputSelectize
                            ref="roles"
                            :elId="getNewElUid()"
                            :cfg="roleCfg"
                            placeholder="All roles"
                            @selected="updateFilters($event, 'roles')"
                        />
                    </div>
                    <div class="col-12 col-md filter-item">
                        <InputSelectize
                            ref="countries"
                            :elId="getNewElUid()"
                            :cfg="countryCfg"
                            placeholder="All countries"
                            @selected="updateFilters($event, 'countries')"
                        />
                    </div>
                    <div v-if="isShowStateSel" class="col-12 col-md filter-item">
                        <InputSelectize
                            ref="states"
                            :elId="getNewElUid()"
                            :cfg="stateCfg"
                            placeholder="All states"
                            @selected="updateFilters($event, 'states')"
                        />
                    </div>
                    <div v-if="isShowStateSel" class="col-12 col-md filter-item">
                        <InputSelectize
                            ref="employers"
                            :elId="getNewElUid()"
                            :cfg="employerCfg"
                            :isParseAsInt="true"
                            placeholder="All employers"
                            @selected="updateFilters($event, 'employers')"
                        />
                    </div>
                    <div class="col-12 col-md filter-item d-flex align-items-center">
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
                        <div class="job-role -color-darkblue -color-white-text">{{ job.role }}</div>
                    </div>
                    <div class="row">
                        <div class="col-md-2 d-flex align-items-center justify-content-center">
                            <img v-if="getEmployer(job.employerId).logo" :src="getEmployer(job.employerId).logo"
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
                                        <a class="btn btn-primary" :href="selectedJob.applicationUrl" target="_blank"
                                           title="This will take you to the company's job application page">
                                            Apply <i class="fas fa-external-link-alt -color-white-text"></i>
                                        </a>
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
</template>

<script>
import AccordionItem from "../../components/AccordionItem";
import BaseFilter from "../base/BaseFilter";
import BasePage from "../base/BasePage";
import dataUtil from "../../../utils/data";
import InputCheckBox from "../../inputs/InputCheckBox";
import InputSelectize from "../../inputs/InputSelectize";
import JobPosting from "../jobPosting/JobPosting";
import Pagination from "../../components/Pagination";
import ListFontAwesome from "../../components/ListFontAwesome";
import JobHelpLinks from "./JobHelpLinks";

export default {
    name: "JobsPage",
    components: {
        JobHelpLinks,
        ListFontAwesome,
        JobPosting, AccordionItem, BaseFilter, BasePage, InputCheckBox, InputSelectize, Pagination
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
            selectedJob: null
        }
    },
    computed: {
        roleCfg() {
            return {
                valueField: 'value',
                labelField: 'value',
                sortField: 'value',
                maxItems: null,
                plugins: ['remove_button'],
                options: this.initData.roles.map((r) => ({value: r}))
            };
        },
        countryCfg() {
            return {
                valueField: 'value',
                labelField: 'value',
                sortField: 'value',
                maxItems: null,
                plugins: ['remove_button'],
                options: this.initData.countries.map((c) => ({value: c}))
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
                valueField: 'value',
                labelField: 'value',
                sortField: 'value',
                maxItems: null,
                plugins: ['remove_button'],
                options: this.initData.states.map((s) => ({value: s}))
            };
        },
        jobs() {
            return this.initData.jobs.filter((j) => {
                if (this.filter.roles?.length && !this.filter.roles.includes(j.role)) {
                    return false;
                }
                if (this.filter.countries?.length && !this.filter.countries.includes(j.country)) {
                    return false;
                }
                if (this.filter.states?.length && !this.filter.states.includes(j.state)) {
                    return false;
                }
                if (this.filter.employers?.length && !this.filter.employers.includes(j.employerId)) {
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
        isShowStateSel() {
            return (
                !this.filter.isRemote
                && (
                    !this.filter?.countries?.length
                    || this.filter.countries.filter((country) => ['USA', 'Canada'].includes(country)).length
                )
            );
        }
    },
    methods: {
        getQueryParams: dataUtil.getQueryParams,
        getEmployer(employerId) {
            return this.initData['employers'][employerId];
        },
        getLocationStr(job) {
            if (job.isRemote) {
                return `Remote: ${job.region || 'Anywhere'}`;
            }
            return ['city', 'state', 'country'].reduce((locationStr, locationPart) => {
                const locationPartStr = dataUtil.get(job, locationPart);
                if (!locationPartStr) {
                    return locationStr;
                }
                if (locationStr === '') {
                    locationStr = locationPartStr;
                } else {
                    locationStr += `, ${locationPartStr}`;
                }
                return locationStr
            }, '');
        },
        showJobDetails(e, job) {
            e.preventDefault();
            this.selectedJob = job;

        },
        updateFilters(val, filterKey) {
            this.setFilter(val, filterKey);
            if (!this.isShowStateSel) {
                this.setFilter(null, 'states');
            }

            // Update the available options based on other filters
            const options = {roles: new Set(), countries: new Set(), employers: new Set(), states: new Set()};
            this.jobs.forEach((job) => {
                options.roles.add(job.role);
                options.states.add(job.state);
                options.countries.add(job.country);
                options.employers.add(this.initData.employers[job.employerId])
            });
            ['roles', 'countries', 'employers', 'states'].forEach((ref) => {
                // Don't update options for the current selectize. Otherwise all other options will be removed.
                if (ref === filterKey && val && val.length) {
                    return;
                }
                const sel = this.$refs[ref];
                if (sel) {
                    let selOptions = Array.from(options[ref]);
                    if (ref !== 'employers') {
                        selOptions = selOptions.map((o) => ({value: o}));
                    }
                    sel.resetOptions(selOptions);
                }
            });

            const pagination = this.$refs.jobsPagination;
            if (pagination) {
                pagination.reset(); // Reset page counts
            }
        }
    },
    mounted() {
        const queryParams = dataUtil.getQueryParams();
        this.$refs.roles.elSel.setValue(queryParams.roles);
        this.$refs.states.elSel.setValue(queryParams.states);
        this.$refs.countries.elSel.setValue(queryParams.countries);
        this.$refs.employers.elSel.setValue(queryParams.employers);
        this.filter.isRemote = queryParams.isRemote === 'true';
    }
}
</script>