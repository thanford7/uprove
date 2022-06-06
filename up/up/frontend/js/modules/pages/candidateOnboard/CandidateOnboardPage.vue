<template>
    <BasePage>
            <div v-if="progressIdx === 0" class="row mb-3 mt-3 justify-content-center">
                <div class="card-custom col-md-8">
                    <p>
                        Hi {{globalData.uproveUser.firstName}}! Welcome to Uprove!
                    </p>
                    <p>
                        At Uprove we help individuals like you showcase your Customer Success skills and upskill to find
                        new opportunities or perform better in your current role.
                    </p>
                    <p>
                        To help us match you with the best opportunities, we have a few questions:
                    </p>
                </div>
            </div>
            <div class="row mb-3 mt-3 justify-content-center">
                <div class="card-custom col-md-8">
                    <div class="form-container ps-4 pe-4">
                        <template v-if="progressIdx === 0">
                            <h5 class="mb-4 text-center">Select the company employee sizes you're interested in</h5>
                            <div class="d-flex justify-content-center">
                                <div class="btn-group" role="group">
                                    <button
                                        v-for="c in initData.companySizes"
                                        type="button"
                                        class="btn btn-outline-dark outline"
                                        @click="toggleSelection($event, c.id, 'companySizes')"
                                    >
                                        {{c.companySize}}
                                    </button>
                                </div>
                            </div>
                        </template>
                        <template v-if="progressIdx === 1">
                            <h5 class="mb-4 text-center">Select the countries you want to work in</h5>
                            <div class="d-flex justify-content-center">
                                <button
                                    v-for="c in initData.countries"
                                    type="button"
                                    class="btn btn-outline-dark outline me-1 mb-1"
                                    @click="toggleSelection($event, c.id, 'countries')"
                                >
                                    {{c.countryName}}
                                </button>
                            </div>
                        </template>
                        <template v-if="progressIdx === 2">
                            <h5 class="mb-4 text-center">What are your preferences on working remotely?</h5>
                            <div class="d-flex justify-content-center">
                                <div class="btn-group" role="group">
                                    <button
                                        type="button"
                                        class="btn btn-outline-dark outline"
                                        @click="toggleValue($event, 2, 'remote')"
                                    >
                                        Remote only
                                    </button>
                                    <button
                                        type="button"
                                        class="btn btn-outline-dark outline"
                                        @click="toggleValue($event, 1, 'remote')"
                                    >
                                        In-person/hybrid only
                                    </button>
                                    <button
                                        type="button"
                                        class="btn btn-outline-dark outline"
                                        @click="toggleValue($event, 3, 'remote')"
                                    >
                                        Either
                                    </button>
                                </div>
                            </div>
                        </template>
                        <template v-if="progressIdx === 3">
                            <h5 class="mb-4 text-center">
                                What your minimum acceptable salary?
                                <InfoToolTip :elId="getNewElUid()" content="We will never show this to employers. We use it to filter out jobs that won't be of interest to you."/>
                            </h5>
                            <div class="d-flex justify-content-center">
                                <RangeSlider
                                    :elId="getNewElUid()"
                                    :min="30000" :max="250000" title="Salary"
                                    :isPct="false" :step="5000" :valueFormatFn="formatCurrency"
                                    @changed="formData.salary = $event"
                                />
                            </div>
                        </template>
                    </div>
                    <div class="row mt-4 pt-2 -border-top--light">
                        <div class="col">
                            <div v-if="progressIdx !== 0" class="btn btn-secondary" @click="progress(-1)">
                                <i class="fas fa-arrow-left"></i> Back
                            </div>
                            <div
                                v-if="progressIdx === progressSteps - 1"
                                class="btn btn-primary float-end"
                                @click="saveChange"
                            >
                                Finish
                            </div>
                            <div v-else class="btn btn-primary float-end" @click="progress(1)">
                                Next <i class="fas fa-arrow-right -color-white-text"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
    </BasePage>
</template>

<script>
import {SEVERITY} from '../../../globalData';
import BannerAlert from '../../components/BannerAlert';
import PageHeader from '../../components/PageHeader';
import BasePage from '../base/BasePage';
import InfoToolTip from "../../components/InfoToolTip";
import RangeSlider from "../../components/RangeSlider";
import dataUtil from "../../../utils/data";

export default {
    name: "CandidateOnboardPage",
    components: {RangeSlider, InfoToolTip, BasePage, BannerAlert, PageHeader},
    data() {
        return {
            crudUrl: 'user-preferences/',
            progressIdx: 0,
            progressSteps: 4,
            progressItems: ['companySizes', 'countries', 'remote', 'salary'],
            formData: {
                companySizes: [],
                countries: [],
                remote: null,
                salary: null
            },
            pageRedirect: '/candidateDashboard/'
        }
    },
    methods: {
        formatCurrency: dataUtil.formatCurrency,
        getAjaxCfgOverride() {
            return {method: 'PUT'};
        },
        progress(change) {
            const formField = this.formData[this.progressItems[this.progressIdx]]
            if (change > 0 && (!formField || (Array.isArray(formField) && !formField.length))) {
                this.addPopover($('.form-container'),
                    {severity: SEVERITY.WARN, content: 'Please select at least one option', isOnce: true}
                );
                return;
            }
            this.progressIdx += change;
        },
        toggleSelection(e, newId, dataKey) {
            const initialLength = this.formData[dataKey].length;

            // Remove the ID if it's already in the list
            this.formData[dataKey] = this.formData[dataKey].filter((id) => id !== newId);

            // Add the ID if it's new
            if (initialLength === this.formData[dataKey].length) {
                this.formData[dataKey].push(newId);
            }

            // Toggle the button on/off
            const targetEl$ = $(e.currentTarget);
            if (targetEl$.hasClass('outline')) {
                targetEl$.toggleClass('btn-outline-dark');
            } else {
                targetEl$.toggleClass('btn-secondary');
            }
            targetEl$.toggleClass('btn-info');
        },
        toggleValue(e, value, dataKey) {
            this.formData[dataKey] = value;

            const btn$ = $(e.currentTarget);
            btn$.addClass('btn-info');
            const btnGroup$ = btn$.siblings('.btn');
            btnGroup$.removeClass('btn-info');
            btnGroup$.addClass('btn-outline-dark');
        }
    }
}
</script>