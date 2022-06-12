<template>
    <div id="home-page">
        <div>
            <div class="container-lg content">
                <div class="row mt-5 align-items-center" :class="(isMobile) ? 'mobile-top' : ''">
                    <BannerAlert/>
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
                <div class="row mt-4 pb-4 justify-content-center">
                    <div class="col-12">
                        <h3 class="mb-4">
                            At Uprove, your success is our success
                        </h3>
                    </div>
                    <div class="col-md-4">
                        <Testimonial :headshotUrl="globalData.STATIC_URL + 'img/headshots/brittanyNewmanHeadshot.jpeg'">
                            Uprove is a great resource for candidates wishing to break into Customer Success.
                            I have referred colleagues and former employees to Uprove to help them grow in their Customer Success career.
                            <template v-slot:name>Brittany Newman</template>
                            <template v-slot:title>Customer Success Manager, True Footage</template>
                        </Testimonial>
                    </div>
                    <div class="col-md-4">
                        <Testimonial :headshotUrl="globalData.STATIC_URL + 'img/headshots/hannaFloresHeadshot.jpeg'">
                            The Uprove team is great! I'm a firm believer in showcasing my work using projects and
                            I'm constantly learning through online training. This has really helped me out with my job search.
                            <template v-slot:name>Hanna Flores</template>
                            <template v-slot:title>Social Services Manager, Alameda County</template>
                        </Testimonial>
                    </div>
                    <div class="col-md-4">
                        <Testimonial :headshotUrl="globalData.STATIC_URL + 'img/headshots/kimberlyJonesHeadshot.jpeg'">
                            Uprove provided insights to help me transition into a new career, and was a valuable
                            resource in my quest to upskill and improve my job search strategy.
                            <template v-slot:name>Kimberly Jones</template>
                            <template v-slot:title>Account Manager, Emsi Burning Glass</template>
                        </Testimonial>
                    </div>
                </div>
            </div>
            <div class="content -color-lightgrey__light mt-4 pt-5 pb-5">
                <div class="container-lg">
                    <div class="row justify-content-center">
                        <div class="mb-md-3 col-12">
                            <h3>Ready to take your Customer Success career to the next level?</h3>
                            <h5>Join the waitlist for the Customer Success Bootcamp (August 8-10)</h5>
                        </div>
                        <div class="col-md-6 mt-2">
                            <img
                                :src="globalData.STATIC_URL + 'img/customerSuccessBootcamp.png'"
                                alt="Customer success bootcamp"
                                :style="(isMobile) ? 'max-height: 25vh' : ''"
                            >
                            <div class="mt-3">
                                <h5>
                                    <i class="fas fa-plus -color-green-text"></i> 3-Day Live, Virtual Bootcamp
                                </h5>
                                <h5>
                                    <i class="fas fa-plus -color-green-text"></i> Certificate of Completion
                                </h5>
                                <h5>
                                    <i class="fas fa-plus -color-green-text"></i> 1-on-1 Resume Review
                                </h5>
                                <h5>
                                    <i class="fas fa-plus -color-green-text"></i> 1-on-1 Skills Gap Assessment
                                </h5>
                            </div>
                        </div>
                        <div class="col-md-6 mt-2">
                            <div class="mb-3">
                                <h6>This class is for:</h6>
                                <ListFontAwesome
                                    faClassesStr="fas fa-check-circle"
                                    faColor="green"
                                    :items="[
                                        'Professionals with 2+ years of experience that want to switch into Customer Success',
                                        'Customer Success Professionals that want to improve their skill set',
                                        'Customer Success Leaders that want to improve their team'
                                    ]"
                                />
                            </div>
                            <div class="mb-3">
                                <h6>Course curriculum:</h6>
                                <ListFontAwesome
                                    faClassesStr="fas fa-award"
                                    faColor="green"
                                    :items="[
                                        'Navigating the phases of the customer journey',
                                        'Project management during implementation',
                                        'Data analysis using Excel',
                                        'Key performance indicators',
                                        'Effective sales - upselling and cross selling',
                                        'Making presentations',
                                        'Public speaking',
                                        'SaaS 101',
                                        'Indirect management',
                                        'Much more...'
                                    ]"
                                />
                            </div>
                        </div>
                        <div class="col-12 mt-2">
                            <div class="row">
                                <div class="mb-3 col-md-6 col-12">
                                    <input type="text" class="form-control" placeholder="Full name" id="userName" v-model="formData.fullName">
                                </div>
                                <div class="mb-3 col-md-6 col-12">
                                    <InputEmail elId="userEmail" placeholder="Email" v-model="formData.email"/>
                                </div>
                                <div class="col-12">
                                    <button type="button" class="btn btn-lg btn-primary button-interactive w-100" @click="joinWaitlist">
                                        Join waitlist and get curriculum
                                        <div class="-text-small">(limit 10 students)</div>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import {SEVERITY} from '../../../globalData';
import {getAjaxFormData, makeAjaxRequest} from "../../../vueMixins";
import BannerAlert from "../../components/BannerAlert";
import dataUtil from "../../../utils/data";
import CardPricing from "../../components/CardPricing";
import EditUserModal from "../../modals/EditUserModal";
import InputEmail from "../../inputs/InputEmail";
import ListFontAwesome from "../../components/ListFontAwesome";
import LearnMore from "./LearnMore";
import OrderedList from '../../components/OrderedList.vue';
import CompanyLogos from "./CompanyLogos";
import Testimonial from "./Testimonial";
import InfoToolTip from "../../components/InfoToolTip";

export default {
    components: {
        InfoToolTip,
        Testimonial,
        CompanyLogos,
        BannerAlert,
        CardPricing,
        EditUserModal,
        InputEmail,
        LearnMore,
        ListFontAwesome,
        OrderedList
    },
    methods: {
        openProjectsPage() {
            window.open('/projects/', '_blank').focus();
        },
        joinWaitlist(e) {
            if (!this.formData.fullName) {
                this.addPopover($('#userName'),
                    {severity: SEVERITY.WARN, content: 'Required field', isOnce: true}
                );
                return;
            }
            if (!this.formData.email) {
                this.addPopover($('#userEmail'),
                    {severity: SEVERITY.WARN, content: 'Required field', isOnce: true}
                );
                return;
            }
            makeAjaxRequest(`${this.apiUrl}waitlist/`, {
                method: 'POST',
                data: getAjaxFormData({
                    waitlistType: 'bootcamp',
                    name: this.formData.fullName,
                    email: this.formData.email
                }),
                success: () => {
                    this.addAlert({
                        message: 'You\'re on the waitlist! Check your email for the course curriculum.',
                        alertType: SEVERITY.SUCCESS
                    });
                },
                error: this.onSaveFailure
            });
            this.formData = {};
        },
        signUpWithContext(waitlistType) {
            dataUtil.signUpWithContext(this.initData, waitlistType);
        }
    },
}
</script>