<template>
    <div id="home-page">
        <div>
            <div class="container-lg content">
                <div class="row mt-5 align-items-center" :class="(isMobile) ? 'mobile-top' : ''">
                    <div class="col-md-7 col-12 justify-content-center">
                        <h1 class="fw-bolder">Find the best Customer Success jobs and grow professionally</h1>
                        <div class="mt-4 -text-large">
                            We help Customer Success professionals be successful - jobs, training, events, and resources
                        </div>
                        <div class="mt-4">
                            <button type="button" class="btn btn-lg btn-primary button-interactive" @click="signUpWithContext">
                                Create account
                            </button>
                        </div>
                        <div class="mt-3">
                            Looking to hire or train your CS team? <a href="/employers/" class="-text-bold">For employers</a>
                        </div>
                    </div>
                    <div class="col-md-5 col-12 p-4">
                        <div class="d-flex justify-content-center">
                            <img
                                :src="globalData.STATIC_URL + 'img/icons/skill-512.png'"
                                alt="Customer success skills"
                                :style="(isMobile) ? 'max-height: 25vh' : ''"
                            >
                        </div>
                    </div>
                </div>
                <CompanyLogos/>
            </div>
            <div class="content -color-lightgrey__light mt-4 pt-5 pb-5">
                <div class="container-lg">
                    <div class="row">
                    <h3 class="mb-4 mb-md-2">
                        The only platform you need to grow your Customer Success career
                    </h3>
                    <div class="row mt-3 justify-content-center" :class="(isMobile) ? 'mobile-top' : ''">
                        <div class="col-md-6">
                            <h5>Put your job search on autopilot</h5>
                            <div class="-text-large">
                                Receive curated job recommendations and get discovered by employers who rely on Uprove to find
                                the most talented Customer Success professionals
                            </div>
                        </div>
                        <div class="col-md-4 mb-4 mb-md-0">
                            <div class="d-flex justify-content-center">
                                <img
                                    :src="globalData.STATIC_URL + 'img/icons/talent-search-512.png'"
                                    alt="Talent"
                                    :style="(isMobile) ? 'max-height: 20vh' : 'max-height: 256px;'"
                                >
                            </div>
                        </div>
                    </div>
                    <div class="row mt-6 justify-content-center">
                        <div class="col-md-4 mb-4 mb-md-0">
                            <div class="d-flex justify-content-center">
                                <img
                                    :src="globalData.STATIC_URL + 'img/icons/feedback-512.png'"
                                    alt="Feedback"
                                    :style="(isMobile) ? 'max-height: 20vh' : 'max-height: 256px;'"
                                >
                            </div>
                        </div>
                        <div class="col-md-6">
                            <h5>Upskill for the most relevant Customer Success skills</h5>
                            <div class="-text-large">
                                Learn from the best Customer Success courses to round out your skills and level up your career
                            </div>
                        </div>
                    </div>
                    <div class="row mt-6 justify-content-center" :class="(isMobile) ? 'mobile-top' : ''">
                        <div class="col-md-6">
                            <h5>Join a community of Customer Success professionals</h5>
                            <div class="-text-large">
                                Get access to exclusive networking events, training resources, and industry news
                            </div>
                        </div>
                        <div class="col-md-4 mb-4 mb-md-0">
                            <div class="d-flex justify-content-center">
                                <img
                                    :src="globalData.STATIC_URL + 'img/icons/network-512.png'"
                                    alt="Community"
                                    :style="(isMobile) ? 'max-height: 20vh' : 'max-height: 256px;'"
                                >
                            </div>
                        </div>
                    </div>
                </div>
                </div>
            </div>
            <div class="container-lg content">
                <div class="row mt-7 mb-5 justify-content-center">
                    <div class="mb-md-3">
                        <h3>Ready to take your Customer Success career to the next level?</h3>
                        <h6>Join a professional community of Customer Success experts</h6>
                    </div>
                    <div class="col-md-4">
                        <CardPricing colorScheme="orange" :buttonClickFn="() => signUpWithContext">
                            <template v-slot:front-header>Community</template>
                            <template v-slot:front-header-explainer>
                                Free to join and get access to great resources
                            </template>
                            <template v-slot:front-price>
                                <h2 class="-color-orange-text">Free</h2>
                            </template>
                            <template v-slot:front-details>
                                <p><b>Everything you need</b></p>
                                <ListFontAwesome
                                    faClassesStr="fas fa-bullseye"
                                    faColor="orange"
                                    :items="[
                                            'Jobs board to find your next job',
                                            'Profile to allow employers to find and hire you',
                                            'Introductory Customer Success training courses',
                                            'Webinars and Customer Success resources',
                                            'A la carte pricing for premium training and events'
                                        ]"
                                />
                            </template>
                            <template v-slot:front-btn-text>Create account</template>
                        </CardPricing>
                    </div>
                    <div class="col-md-4">
                        <CardPricing colorScheme="darkblue" :buttonClickFn="() => signUpWithContext">
                            <template v-slot:front-header>Professional</template>
                            <template v-slot:front-header-explainer>
                                Get premium resources to advance your Customer Success career
                            </template>
                            <template v-slot:front-price>
                                <h2 class="-color-darkblue-text">$100/mo</h2>
                            </template>
                            <template v-slot:front-details>
                                <p><b>Premium resources</b></p>
                                <ListFontAwesome
                                    faClassesStr="fas fa-bullseye"
                                    faColor="darkblue"
                                    :items="[
                                            'Premium Customer Success training courses',
                                            'Certificates of completion for all training courses',
                                            'Exclusive webinars and events',
                                            'One-on-one resume review with a Customer Success expert',
                                            'Cancel at any time'
                                        ]"
                                />
                            </template>
                            <template v-slot:front-btn-text>Sign up</template>
                        </CardPricing>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import BannerAlert from "../../components/BannerAlert";
import dataUtil from "../../../utils/data";
import CardPricing from "../../components/CardPricing";
import EditUserModal from "../../modals/EditUserModal";
import ListFontAwesome from "../../components/ListFontAwesome";
import LearnMore from "./LearnMore";
import OrderedList from '../../components/OrderedList.vue';
import CompanyLogos from "./CompanyLogos";

export default {
    components: {
        CompanyLogos,
        BannerAlert,
        CardPricing,
        EditUserModal,
        LearnMore,
        ListFontAwesome,
        OrderedList
    },
    methods: {
        openProjectsPage() {
            window.open('/projects/', '_blank').focus();
        },
        signUpWithContext() {
            dataUtil.signUpWithContext(this.initData);
        }
    },
}
</script>