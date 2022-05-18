<template>
    <div id="employer-page">
        <EmployerSalesMagnet v-if="showMagnet" @close="showMagnet = false"/>
        <div class="overlap-bottom-side -z-50">
            <div class="container-lg content">
                <div class="row mt-3 justify-content-center">
                    <div class="col-md-4 employer-benefits">
                        <div class="row mb-4"
                             @mouseenter="triggerImgClass(3, true)"
                             @mouseleave="triggerImgClass(3, false)"
                        >
                            <div class="col-2">
                                <img :src="globalData.STATIC_URL + 'img/icons/talent-search.png'">
                            </div>
                            <div class="col-10">
                                <h5>Discover hidden talent in seconds</h5>
                                Easily find candidates by searching based on role (e.g. business analyst),
                                skills (e.g. Excel), and comparable experience level. Narrow down candidates based on their project
                                performance.
                            </div>
                        </div>
                        <div class="row mb-4"
                             @mouseenter="triggerImgClass(2, true)"
                             @mouseleave="triggerImgClass(2, false)"
                        >
                            <div class="col-2">
                                <img :src="globalData.STATIC_URL + 'img/icons/skills.png'">
                            </div>
                            <div class="col-10">
                                <h5>Receive verified, standardized reviews of candidates</h5>
                                Our industry experts review all candidates based on standardized criteria for each project so
                                you know you're getting the best talent and there is no bias in the selection process.
                            </div>
                        </div>
                        <div class="row mb-4"
                             @mouseenter="triggerImgClass(1, true)"
                             @mouseleave="triggerImgClass(1, false)"
                        >
                            <div class="col-2">
                                <img :src="globalData.STATIC_URL + 'img/icons/online-interview.png'">
                            </div>
                            <div class="col-10">
                                <h5>Manage all of your talent in one simple dashboard</h5>
                                Review, approve, and decline applicants in a centralized dashboard or talk to us about
                                integrating with your existing applicant tracking system.
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 ps-md-5">
                        <div class="collage">
                            <img :src="globalData.STATIC_URL + 'img/employerDashboardExample.png'"
                                @mouseenter="triggerDivClass(3, true)"
                                @mouseleave="triggerDivClass(3, false)"
                            >
                            <img :src="globalData.STATIC_URL + 'img/projectEvaluationExample.png'"
                                @mouseenter="triggerDivClass(2, true)"
                                @mouseleave="triggerDivClass(2, false)"
                            >
                            <img :src="globalData.STATIC_URL + 'img/candidateBoardExample.png'"
                                @mouseenter="triggerDivClass(1, true)"
                                @mouseleave="triggerDivClass(1, false)"
                            >
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="overlap-final-employer -z-40">
            <div class="container-lg content">
                <div class="row justify-content-center">
                    <div class="col-md-4">
                        <CardPricing colorScheme="orange" :buttonClickFn="() => redirectUrl('/sign-up/employer/prove/')">
                            <template v-slot:front-header>Prove it package</template>
                            <template v-slot:front-header-explainer>
                                No risk, just proving it. We can show you the hidden talent you are missing.
                            </template>
                            <template v-slot:front-price>
                                <h2 class="-color-orange-text">$0/mo</h2>
                                <h6>20% first year salary fee per hire</h6>
                                <h6>No contract term</h6>
                            </template>
                            <template v-slot:front-details>
                                <p><b>Everything you need</b></p>
                                <ListFontAwesome
                                    faClassesStr="fas fa-ghost"
                                    faColor="orange"
                                    :items="[
                                        'Access to all projects',
                                        'Access to all candidates',
                                        'Dedicated talent expert',
                                        'Unlimited job postings',
                                        'Applicant interview fast tracking'
                                    ]"
                                />
                            </template>
                            <template v-slot:front-btn-text>Get started with a talent expert</template>
                        </CardPricing>
                    </div>
                    <div class="col-md-4">
                        <CardPricing colorScheme="darkblue" :buttonClickFn="() => redirectUrl('/sign-up/employer/')">
                            <template v-slot:front-header>Improve it package</template>
                            <template v-slot:front-header-explainer>
                                Partner with us and save immediately. Great for teams making more than one hire per month.
                            </template>
                            <template v-slot:front-price>
                                <h2 class="-color-darkblue-text">Custom price/mo</h2>
                                <h6>No fee per hire</h6>
                                <h6>Monthly contract</h6>
                            </template>
                            <template v-slot:front-details>
                                <p><b>Everything you need and more</b></p>
                                <ListFontAwesome
                                    faClassesStr="fas fa-ghost"
                                    faColor="darkblue"
                                    :items="[
                                        'Advanced analytics to track candidates',
                                        'Customized projects',
                                        'Promoted job posts'
                                    ]"
                                />
                            </template>
                            <template v-slot:front-btn-text>Talk to sales team</template>
                        </CardPricing>
                    </div>
                </div>
            </div>
        </div>
        <div>
            <div class="container-lg content -overlap-top-4">
                <div class="row justify-content-center">
                    <div class="col-md-6 card-custom card-custom--shadow -z-50">
                        <h3 class="fw-bold mb-4">
                            <span style="display: inline-block">Get started now to find</span>
                            <span class="-color-orange-text" style="display: inline-block">hidden talent</span>
                        </h3>
                        <BannerAlert/>
                        <EmployerRequestInfoModal ref="employerRequest" :isContentOnly="true"/>
                        <button @click="$refs['employerRequest'].saveChange($event)" type="button" class="btn btn-primary button-interactive mt-3 w-100">Talk to a talent expert</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import BannerAlert from "../../components/BannerAlert";
import BasePage from "../base/BasePage";
import CardPricing from "../../components/CardPricing";
import EmployerRequestInfoModal from "../../modals/EmployerRequestInfoModal";
import EmployerSalesMagnet from "./EmployerSalesMagnet";
import ListFontAwesome from "../../components/ListFontAwesome";

export default {
    name: "EmployersPage",
    components: {BannerAlert, BasePage, CardPricing, EmployerRequestInfoModal, EmployerSalesMagnet, ListFontAwesome},
    data() {
        return {
            showMagnet: false
        }
    },
    methods: {
        toggleClass(target, notTarget, isOn) {
            target.toggleClass('sibling-hover', isOn);
            target.toggleClass('not-sibling-hover', !isOn);
            notTarget.toggleClass('not-sibling-hover', isOn);
        },
        triggerImgClass(imgIdx, isOn) {
            const targetImg = $(`.collage img:nth-child(${imgIdx})`);
            const notTargetImg = $(`.collage img:not(:nth-child(${imgIdx}))`);
            this.toggleClass(targetImg, notTargetImg, isOn);
        },
        triggerDivClass(divIdx, isOn) {
            const targetDiv = $(`.employer-benefits .row:nth-child(${divIdx})`);
            const notTargetDiv = $(`.employer-benefits .row:not(:nth-child(${divIdx}))`);
            this.toggleClass(targetDiv, notTargetDiv, isOn);
        }
    },
    mounted() {
        // Add 10 seconds then show sales magnet
        setTimeout(() => {
            this.showMagnet = true;
        }, 10000);
    }
}
</script>