<template>
    <BasePage>
            <div v-if="progressIdx === 0" class="row mb-3 mt-3 justify-content-center">
                <div class="card-custom col-md-8">
                    <p>
                        Hi {{globalData.uproveUser.firstName}}! Welcome to Uprove!
                    </p>
                    <p>
                        At Uprove we help individuals like you showcase their talent and connect with employers seeking candidates
                        with your skill set. Complete one or more of our skills based exercises to show employers what you're
                        made of and secure your next opportunity!
                    </p>
                    <p>
                        To help us match you with the best opportunities and recommend real world business cases to help you
                        showcase your talent, we have a few questions:
                    </p>
                </div>
            </div>
            <div class="row mb-3 mt-3 justify-content-center">
                <div class="card-custom col-md-8">
                    <div class="row justify-content-center ps-4 pe-4">
                        <template v-if="progressIdx === 0">
                            <h5 class="mb-4 text-center">Select the company employee sizes you're interested in</h5>
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
                        </template>
                        <template v-if="progressIdx === 1">
                            <h5 class="mb-4 text-center"></h5>
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
                        </template>
                    </div>
                    <div class="row mt-4 pt-2 -border-top--light">
                        <div class="col">
                            <div v-if="progressIdx !== 0" class="btn btn-secondary" @click="progressIdx--">
                                <i class="fas fa-arrow-left"></i> Back
                            </div>
                            <div class="btn btn-primary float-end" @click="progressIdx++">
                                Next <i class="fas fa-arrow-right -color-white-text"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
    </BasePage>
</template>

<script>
import BannerAlert from "../../components/BannerAlert";
import dataUtil from "../../../utils/data";
import PageHeader from "../../components/PageHeader";
import BasePage from "../base/BasePage";

export default {
    name: "CandidateOnboardPage",
    components: {BasePage, BannerAlert, PageHeader},
    data() {
        return {
            progressIdx: 0,
            progressSteps: 5,
            companySizes: []
        }
    },
    methods: {
        toggleSelection(e, newId, dataKey) {
            const initialLength = this[dataKey].length;

            // Remove the ID if it's already in the list
            this[dataKey] = this[dataKey].filter((id) => id !== newId);

            // Add the ID if it's new
            if (initialLength === this[dataKey].length) {
                this[dataKey].push(newId);
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
    }
}
</script>