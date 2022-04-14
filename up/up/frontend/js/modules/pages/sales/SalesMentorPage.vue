<template>
    <div>
        <p class="alert fade show alert-warning -color-darkblue-text text-center sticky-top mb-0" role="alert">
            Sign up by April 8th and we'll send you a link to our free course, <b>"How to Land Any Job"</b><br/>
            Time remaining: {{offerTimeRemaining}}
        </p>
        <div class="-color-white">
            <div class="container-lg">
                <div class="row pt-4 pb-4">
                    <img class="logo" :src="globalData.STATIC_URL + 'img/logo.png'" alt="Uprove" style="max-width: 200px;">
                </div>
                <div class="content row align-items-center">
                    <div class="col-md-7 ps-md-5 pe-md-6">
                        <div class="p-md-4">
                            <h1 id="header-main" class="-color-darkblue-text">
                                Professional feedback from hiring managers
                            </h1>
                            <h5 class="mt-4">
                                Want to know why you aren't getting a job offer? Get candid feedback from actual hiring managers
                            </h5>
                            <div class="mt-4">
                                <BannerAlert/>
                                <div class="input-group mb-3">
                                    <InputEmail
                                        ref="email"
                                        :elId="getNewElUid()"
                                        class="-color-lightgrey__light"
                                        placeholder="Your email..."
                                        @keyup.enter="saveWaitlist"
                                        v-model="formData.email"
                                    />
                                    <button class="btn btn-secondary -color-orange" @click="saveWaitlist">
                                        <i class="fas fa-paper-plane"></i>
                                        Join waitlist
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-5 pb-3 -bg-clip-border ps-0 pe-0 d-flex align-items-center">
                        <video class="background-video" autoplay loop muted poster="" style="border-radius: 10px;">
                          <source :src="globalData.STATIC_URL + 'video/interview.mp4'" type="video/mp4">
                        </video>
                    </div>
                </div>
            </div>
        </div>
        <div class="container-lg pt-5 pb-3 ps-md-5 pe-md-6">
            <div class="row">
                <h3 class="-color-darkblue-text">How it works</h3>
                <p>We match you with an experienced hiring manager from companies similar to the ones you are applying to</p>
            </div>
            <div class="row pt-3">
                <div class="col-md-4">
                    <div class="pb-2">
                        <img :src="globalData.STATIC_URL + 'img/icons/032-decision-making.png'">
                    </div>
                    <h5>Pick your hiring coach</h5>
                    <p>Filter coaches based on role, industry, and experience level</p>
                </div>
                <div class="col-md-4">
                    <div class="pb-2">
                        <img :src="globalData.STATIC_URL + 'img/icons/online-interview.png'" style="max-width: 64px;">
                    </div>
                    <h5>Conduct a mock interview</h5>
                    <p>Your hiring coach will spend 30 minutes conducting an interview and another 30 minutes providing feedback</p>
                </div>
                <div class="col-md-4">
                    <div class="pb-2">
                        <img :src="globalData.STATIC_URL + 'img/icons/012-list.png'">
                    </div>
                    <h5>Receive an action plan</h5>
                    <p>After your interview, you will receive a detailed action plan.
                        You can choose to set up additional meetings with your coach to review
                        progress and receive more feedback
                    </p>
                </div>
            </div>
        </div>
        <div class="-color-white pt-5 pb-3">
            <div class="container-lg">
                <h4 class="-color-darkblue-text">You've been submitting your resume to hundreds of job positions,
                    but haven't landed a job and have no idea why...
                </h4>
                <div class="row mt-4">
                    <div class="col-md-8">
                        <div class="row">
                            <div class="col-md-6">
                                <h5>If you're switching careers, figuring out the right roles and companies to target is challenging</h5>
                            </div>
                            <div class="col-md-6">
                                <p>Without direct experience in a specific role, it's tough to determine
                                    the right job titles, experience level, and qualifications that are a good fit for you.
                                    You may be wasting your time applying for jobs where your success rate is close to 0%
                                </p>
                            </div>
                        </div>
                        <div class="row mt-3">
                            <div class="col-md-6">
                                <h5>Resume screening software filters your application with no feedback</h5>
                            </div>
                            <div class="col-md-6">
                                <p>Applicant tracking systems are a "black box" to applicants.
                                    You have no clue whether your resume had the appropriate keywords
                                </p>
                            </div>
                        </div>
                        <div class="row mt-3">
                            <div class="col-md-6">
                                <h5>Hiring managers and staffing agencies won't tell you why they "went another direction"</h5>
                            </div>
                            <div class="col-md-6">
                                <p>Hiring managers have limited time and want to avoid the legal risk of providing direct
                                    feedback. There may have been one little thing to change or you may have a large skill
                                    gap. Either way, you won't know about it
                                </p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <img :src="globalData.STATIC_URL + 'img/icons/filter.png'">
                    </div>
                </div>
            </div>
        </div>
        <div class="container-lg pt-5 pb-3">
            <div class="row justify-content-center">
                <h3 class="col-md-7 -color-darkblue-text">Interviews are too important to leave to chance. Get the inside scoop today.</h3>
                <div class="col-md-6 mt-4">
                    <BannerAlert/>
                    <div class="input-group mb-3">
                        <InputEmail
                            ref="email"
                            :elId="getNewElUid()"
                            class="-color-lightgrey__light"
                            placeholder="Your email..."
                            v-model="formData.email"
                            @keyup.enter="saveWaitlist"
                        />
                        <button class="btn btn-secondary -color-orange" @click="saveWaitlist">
                            <i class="fas fa-paper-plane"></i>
                            Join waitlist
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import BannerAlert from "../../components/BannerAlert";
import dateUtil from "../../../utils/dateUtil";
import dayjs from "dayjs/esm";
import InputEmail from "../../inputs/InputEmail";
import {getAjaxFormData} from "../../../vueMixins";

export default {
    name: "SalesMentorPage",
    components: {BannerAlert, InputEmail},
    data() {
        return {
            formData: {},
            offerTimeRemaining: null,
            offerEndDateTime: '2022-04-08 23:59'
        }
    },
    methods: {
        getAjaxCfgOverride() {
            return {method: 'POST'};
        },
        getSuccessMessage() {
            return 'Thanks for your interest! We added you to the waitlist and sent an email confirmation. If you don\'t' +
                ' see it, please check your spam folder.';
        },
        saveWaitlist() {
            const ajaxData = getAjaxFormData({
                email: this.formData.email,
                waitlistType: 'mentor',
                signUpDateTime: dateUtil.serializeDateTime(dayjs())
            }, []);
            this.submitAjaxRequest(ajaxData, {
                url: this.apiUrl + 'waitlist/',
            });
        }
    },
    mounted() {
        this.offerTimeRemaining = dateUtil.getTimeRemaining(this.offerEndDateTime);
    }
}
</script>