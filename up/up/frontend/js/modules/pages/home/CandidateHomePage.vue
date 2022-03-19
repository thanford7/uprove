<template>
    <div id="home-page">
        <div class="overlap-bottom-side -z-50">
            <div class="container-lg content">
                <div class="row mt-3">
                    <div class="text-center mb-4">
                        <h3 class="-color-linear-text-blue fw-bold">We put you in control of your job search</h3>
                    </div>
                </div>
                <div class="row justify-content-center">
                    <div class="col-md-5 mb-4 mt-3">
                        <div class="feature-box">
                            <div class="call-out">Find</div>
                            <img :src="globalData.STATIC_URL + 'img/icons/020-key-person.png'">
                            <h5 class="header">Reverse resume matching to identify job opportunities where you will rank highest</h5>
                            <p>You spend hours upon hours searching the web for job opportunities. Wouldn't it be nice
                                if they came to you? We are the reverse Applicant Tracking System. We use keywords from
                                your resume to uncover the jobs that you are most likely to get.
                            </p>
                            <button id="lm-reverse-resume" class="btn btn-secondary btn--learn-more">
                                Learn more
                            </button>
                        </div>
                    </div>
                    <div class="col-md-5 mb-4 mt-3">
                        <div class="feature-box">
                            <div class="call-out">Skills align</div>
                            <img :src="globalData.STATIC_URL + 'img/icons/034-success-1.png'">
                            <h5 class="header">Curated, real-world projects to help you demonstrate your skills</h5>
                            <p>You have the skills, but you might not have the background. If you're a career starter
                                or career switcher, getting your foot in the door is hard. Our real world projects help
                                you demonstrate your skills and allow employers to see your true potential.
                            </p>
                            <button id="lm-project" class="btn btn-secondary btn--learn-more">
                                Learn more
                            </button>
                        </div>
                    </div>
                    <div class="col-md-5 mb-4 mt-3">
                        <div class="feature-box">
                            <div class="call-out">Shine</div>
                            <img :src="globalData.STATIC_URL + 'img/icons/027-video-call.png'">
                            <h5 class="header">Easily customizable profile to display your project portfolio</h5>
                            <p>It's tough to stand out when your career is reduced to a single piece of paper and
                                judged by a cold, lifeless Applicant Tracking System. A project portfolio allows you to
                                bring your skills to light with text, images, and videos. There's a reason why coders
                                and designers commonly have a project portfolio: it works!
                            </p>
                            <button id="lm-portfolio" class="btn btn-secondary btn--learn-more">
                                Learn more
                            </button>
                        </div>
                    </div>
                    <div class="col-md-5 mb-4 mt-3">
                        <div class="feature-box">
                            <div class="call-out">Blow their mind</div>
                            <img :src="globalData.STATIC_URL + 'img/icons/021-strategy.png'">
                            <h5 class="header">Advanced interview preparation to wow any employer</h5>
                            <p>It's common for candidates to come to interviews unprepared. We help you shine
                                with mock interview questions and critique, summarized company information so you can
                                be knowledgeable, and recommended questions to ask about the company which will make you
                                look like a genius.
                            </p>
                            <button id="lm-interview" class="btn btn-secondary btn--learn-more">
                                Learn more
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="overlap-final -z-40">
            <div class="container-lg content">
                <div class="row justify-content-center">
                    <div class="col-md-6">
                        <h3 class="fw-bold mb-4">
                            <span style="display: inline-block">Our candidate advocates are standing by to help you</span>
                            <span class="-color-orange-text" style="display: inline-block">prove yourself</span>
                        </h3>
                        <BannerAlert/>
                        <EditUserModal ref="userSignUp" :isContentOnly="true"/>
                        <button @click="$refs['userSignUp'].saveChange($event)" type="button"
                                class="btn btn-primary button-interactive"
                        >
                            Create account
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import BannerAlert from "../../components/BannerAlert";
import dataUtil from "../../../utils/data";
import EditUserModal from "../../modals/EditUserModal";
import OrderedList from '../../components/OrderedList.vue';

export default {
    components: {
        BannerAlert,
        EditUserModal,
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