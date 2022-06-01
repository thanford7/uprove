<template>
    <div id="home-page">
        <div>
            <div class="container-lg content">
                <div class="row mt-5 align-items-center" :class="(isMobile) ? 'mobile-top' : ''">
                    <div class="col-md-7 col-12 justify-content-center">
                        <h1 class="fw-bolder">Find the best customer success jobs and grow professionally</h1>
                        <div class="mt-4 -text-large">
                            We help customer success professionals be successful - jobs, events, and training resources - always free to job candidates
                        </div>
                        <div class="mt-4">
                            <button type="button" class="btn btn-lg btn-primary button-interactive" @click="signUpWithContext">
                                Create account
                            </button>
                        </div>
                        <div class="mt-3">
                            Looking to hire? <a href="/employers/" class="-text-bold">Hire customer success professionals</a>
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
            </div>
            <div class="content -color-lightgrey__light mt-4 pt-5 pb-5">
                <div class="container-lg">
                    <div class="row">
                    <h3 class="mb-4 mb-md-2">
                        The only platform you need to grow your Customer Success career
                    </h3>
                    <div class="row mt-3" :class="(isMobile) ? 'mobile-top' : ''">
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
                    <div class="row mt-6">
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
                            <h5>Get professional feedback</h5>
                            <div class="-text-large">
                                Learn how you can improve your customer success skills and stand out to employers
                            </div>
                        </div>
                    </div>
                    <div class="row mt-6" :class="(isMobile) ? 'mobile-top' : ''">
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
                <div class="row mt-7 mb-5">
                    <div class="mb-md-3">
                        <h3>How it works</h3>
                        <h6>Join a professional community of Community Success experts in four simple steps</h6>
                    </div>
                    <div class="col-md-3 mt-3">
                        <table>
                            <tbody>
                                <tr>
                                    <td style="vertical-align: top;">
                                        <div class="circle circle-inverse circle-small me-3 mt-2">1</div>
                                    </td>
                                    <td>
                                        <h5 class="mb-0">Complete a business case assessment</h5>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <div>The assessment helps showcase your Customer Success skills</div>
                    </div>
                    <div class="col-md-3 mt-3">
                        <table>
                            <tbody>
                                <tr>
                                    <td style="vertical-align: top;">
                                        <div class="circle circle-inverse circle-small me-3 mt-2">2</div>
                                    </td>
                                    <td>
                                        <h5 class="mb-0">Receive direct feedback from an expert</h5>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <div>A Uprove Customer Success Expert will give you guidance on how to improve your Customer Success skills</div>
                    </div>
                    <div class="col-md-3 mt-3">
                        <table>
                            <tbody>
                                <tr>
                                    <td style="vertical-align: top;">
                                        <div class="circle circle-inverse circle-small me-3 mt-2">3</div>
                                    </td>
                                    <td>
                                        <h5 class="mb-0">Get matched with your dream jobs</h5>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <div>We account for your preferences such as location and salary</div>
                    </div>
                    <div class="col-md-3 mt-3">
                        <table>
                            <tbody>
                                <tr>
                                    <td style="vertical-align: top;">
                                        <div class="circle circle-inverse circle-small me-3 mt-2">4</div>
                                    </td>
                                    <td>
                                        <h5 class="mb-0">Access the professional community</h5>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <div>Get access to training resources and events focused on improving your Customer Success skills</div>
                    </div>
                    <div class="mt-4 d-flex justify-content-center">
                        <button type="button" class="btn btn-lg btn-primary button-interactive" @click="signUpWithContext">
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
import LearnMore from "./LearnMore";
import OrderedList from '../../components/OrderedList.vue';

export default {
    components: {
        BannerAlert,
        EditUserModal,
        LearnMore,
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