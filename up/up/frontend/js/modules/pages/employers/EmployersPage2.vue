<template>
    <div id="employer-page">
        <EmployerSalesMagnet v-if="showMagnet" @close="showMagnet = false"/>
        <div class="container-lg content">
            <div class="row mt-5 align-items-center" :class="(isMobile) ? 'mobile-top' : ''">
                <div class="col-md-7 col-12 justify-content-center">
                    <h1 class="fw-bolder">Hire the best Customer Success Professionals</h1>
                    <div class="mt-4 -text-large">
                        Don't leave your customers' happiness to chance. Hire vetted and trained Customer Success
                        Professionals to ensure great relationships with your clients
                    </div>
                    <div class="mt-4">
                        <button type="button" class="btn btn-lg btn-primary button-interactive"
                                @click="() => redirectUrl('/sign-up/employer/prove/')">
                            Start hiring
                        </button>
                    </div>
                </div>
                <div class="col-md-5 col-12 p-4">
                    <div class="d-flex justify-content-center">
                        <img
                            :src="globalData.STATIC_URL + 'img/icons/key-person-512.png'"
                            alt="Best customer success hire"
                            :style="(isMobile) ? 'max-height: 25vh' : ''"
                        >
                    </div>
                </div>
            </div>
        </div>
        <div class="content -color-lightgrey__light mt-4 pt-5 pb-5">
            <div class="container-lg">
                <div class="row">
                    <h3 class="mb-4 mb-md-2">
                        We focus on finding the best Customer Success talent so you can focus on your customers' success
                    </h3>
                    <div class="row mt-3" :class="(isMobile) ? 'mobile-top' : ''">
                        <div class="col-md-6">
                            <h5>Vetted by Customer Success experts</h5>
                            <div class="-text-large">
                                Every job seeker completes a customer success business case and is evaluated by
                                a customer success expert
                            </div>
                        </div>
                        <div class="col-md-4 mb-4 mb-md-0">
                            <div class="d-flex justify-content-center">
                                <img
                                    :src="globalData.STATIC_URL + 'img/icons/candidate-filter-512.png'"
                                    alt="Talent"
                                    :style="(isMobile) ? 'max-height: 20vh' : 'max-height: 256px;'"
                                >
                            </div>
                        </div>
                    </div>
                    <div class="row mt-6">
                        <div class="col-md-4 mb-4 mb-md-0">
                            <div class="d-flex justify-content-center">
                                <img
                                    :src="globalData.STATIC_URL + 'img/icons/training-512.png'"
                                    alt="Feedback"
                                    :style="(isMobile) ? 'max-height: 20vh' : 'max-height: 256px;'"
                                >
                            </div>
                        </div>
                        <div class="col-md-6">
                            <h5>Trained and upskilled for the most important Customer Success skills</h5>
                            <div class="-text-large">
                                All Uprove job seekers have access to educational resources and are required to complete
                                training based on recommendations from a Uprove customer success expert
                            </div>
                        </div>
                    </div>
                    <div class="row mt-6" :class="(isMobile) ? 'mobile-top' : ''">
                        <div class="col-md-6">
                            <h5>Continuous access to Customer Success best practices</h5>
                            <div class="-text-large">
                                Uprove provides live and online customer success events and develops customer success
                                resources based on best practices
                            </div>
                        </div>
                        <div class="col-md-4 mb-4 mb-md-0">
                            <div class="d-flex justify-content-center">
                                <img
                                    :src="globalData.STATIC_URL + 'img/icons/growth-512.png'"
                                    alt="Community"
                                    :style="(isMobile) ? 'max-height: 20vh' : 'max-height: 256px;'"
                                >
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="container-lg content mt-5">
            <div class="row justify-content-center">
                <div class="col-12">
                    <h3 class="text-center mb-3">
                        Start hiring the best Customer Success Professionals
                    </h3>
                </div>
                <div class="col-md-4">
                    <CardPricing colorScheme="orange" :buttonClickFn="() => redirectUrl('/sign-up/employer/prove/')">
                        <template v-slot:front-header>Prove it package</template>
                        <template v-slot:front-header-explainer>
                            No risk, just proving it. Get access to top customer success talent.
                        </template>
                        <template v-slot:front-price>
                            <h2 class="-color-orange-text">$0/mo</h2>
                            <h6>20% first year salary fee per hire</h6>
                            <h6>No contract term</h6>
                        </template>
                        <template v-slot:front-details>
                            <p><b>Everything you need</b></p>
                            <ListFontAwesome
                                faClassesStr="fas fa-bullseye"
                                faColor="orange"
                                :items="[
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
                            <h6>Reduced placement fee</h6>
                            <h6>Monthly contract</h6>
                        </template>
                        <template v-slot:front-details>
                            <p><b>Everything you need and more</b></p>
                            <ListFontAwesome
                                faClassesStr="fas fa-bullseye"
                                faColor="darkblue"
                                :items="[
                                        'ATS integration',
                                        'Promoted job posts',
                                        'Access to premium training content'
                                    ]"
                            />
                        </template>
                        <template v-slot:front-btn-text>Talk to sales team</template>
                    </CardPricing>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import BannerAlert from "../../components/BannerAlert";
import BasePage from "../base/BasePage";
import CardPricing from "../../components/CardPricing";
import EmployerSalesMagnet from "./EmployerSalesMagnet";
import ListFontAwesome from "../../components/ListFontAwesome";

export default {
    name: "EmployersPage",
    components: {BannerAlert, BasePage, CardPricing, EmployerSalesMagnet, ListFontAwesome},
    data() {
        return {
            showMagnet: false
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