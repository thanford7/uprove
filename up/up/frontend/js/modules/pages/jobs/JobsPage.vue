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
                            ref="role"
                            :elId="getNewElUid()"
                            :cfg="roleCfg"
                            placeholder="All roles"
                            @selected="filters.roles = $event"
                        />
                    </div>
                    <div class="col-12 col-md filter-item">
                        <InputSelectize
                            ref="country"
                            :elId="getNewElUid()"
                            :cfg="countryCfg"
                            placeholder="All countries"
                            @selected="filters.countries = $event"
                        />
                    </div>
                    <div v-if="true" class="col-12 col-md filter-item">
                        <InputSelectize
                            ref="state"
                            :elId="getNewElUid()"
                            :cfg="stateCfg"
                            placeholder="All states"
                            @selected="filters.states = $event"
                        />
                    </div>
                </div>
            </BaseFilter>
        </template>
        <div class="jobs row">
            <div v-for="job in initData.jobs" class="card-custom">
                <div class="row">
                    <div class="col-md-2 d-flex align-items-center justify-content-center">
                        <img v-if="getEmployer(job.employerId).logo" :src="getEmployer(job.employerId).logo" class="logo">
                        <i v-else class="far fa-building fa-4x"></i>
                    </div>
                    <div class="col-md-10">
                        <h5>{{job.jobTitle}}</h5>
                        <h6>{{getEmployer(job.employerId).companyName}}</h6>
                        <h6>{{getLocationStr(job)}}</h6>
                    </div>
                </div>
            </div>
        </div>
    </BasePage>
</template>

<script>
import BaseFilter from "../base/BaseFilter";
import BasePage from "../base/BasePage";
import dataUtil from "../../../utils/data";
import InputSelectize from "../../inputs/InputSelectize";

export default {
    name: "JobsPage",
    components: {BaseFilter, BasePage, InputSelectize},
    data() {
        return {
            filters: {
                roles: [],
                countries: [],
                states: []
            }
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
            }
        },
        countryCfg() {
            return {
                valueField: 'value',
                labelField: 'value',
                sortField: 'value',
                maxItems: null,
                plugins: ['remove_button'],
                options: this.initData.countries.map((c) => ({value: c}))
            }
        },
        stateCfg() {
            return {
                valueField: 'value',
                labelField: 'value',
                sortField: 'value',
                maxItems: null,
                plugins: ['remove_button'],
                options: this.initData.states.map((s) => ({value: s}))
            }
        }
    },
    methods: {
        getEmployer(employerId) {
            return this.initData['employers'][employerId];
        },
        getLocationStr(job) {
            if (job.isRemote) {
                return `Remote: ${job.region}`;
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
        }
    }
}
</script>