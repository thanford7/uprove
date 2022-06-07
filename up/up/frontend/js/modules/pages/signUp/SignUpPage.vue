<template>
    <BasePage>
        <div class="row mt-3 mb-3 justify-content-center">
            <div class="col-md-5 card-custom">
                <h5 class="fw-bold">Get started with Uprove</h5>
                <EditUserModal ref="userSignUp" :isContentOnly="true"/>
                <button @click="$refs['userSignUp'].saveChange($event)" type="button" class="btn btn-primary w-100">Create account</button>
            </div>
            <div class="col-md-4 card-custom">
                <h5 class="fw-bold">Sign up for free and join the best Customer Success Professionals!</h5>
                <div class="row mb-3 mt-3">
                    <div class="col-2 d-flex align-items-center">
                        <img :src="globalData.STATIC_URL + 'img/icons/headhunter.png'" class="-max-height-32">
                    </div>
                    <div class="col-10">
                        We save you time by finding
                        <span class="-color-orange-text"><b>jobs that are the best fit for you</b></span>
                    </div>
                </div>
                <div class="row mb-3 mt-3">
                    <div class="col-2 d-flex align-items-center">
                        <img :src="globalData.STATIC_URL + 'img/icons/approved.png'" class="-max-height-32">
                    </div>
                    <div class="col-10">
                        We help you prove yourself by giving you access to the best training resources and real world projects that will
                        <span class="fw-bold -color-orange-text"><b>showcase your skills to employers</b></span>
                    </div>
                </div>
                <div class="row mb-3 mt-3">
                    <div class="col-2 d-flex align-items-center">
                        <img :src="globalData.STATIC_URL + 'img/icons/015-strong.png'" class="-max-height-32">
                    </div>
                    <div class="col-10">
                        We provide training, events, and resources to help you
                        <span class="fw-bold -color-orange-text"><b>stand out</b></span>
                        in your Customer Success profession
                    </div>
                </div>
            </div>
        </div>
    </BasePage>
</template>

<script>
import EditUserModal from "../../modals/EditUserModal";
import BasePage from "../base/BasePage";

export default {
    name: "SignUpPage",
    components: {BasePage, EditUserModal},
}
</script>