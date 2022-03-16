<template>
    <BasePage>
        <div class="row mt-3 mb-3 justify-content-center">
            <div class="col-md-5 card-custom">
                <h5 class="fw-bold">Get started with Uprove</h5>
                <EditUserModal ref="userSignUp" :isContentOnly="true"/>
                <button @click="$refs['userSignUp'].saveChange($event)" type="button" class="btn btn-primary w-100">Create account</button>
            </div>
            <div class="col-md-4 card-custom">
                <h5 class="fw-bold">Sign up for free and take back control of your job search!</h5>
                <div class="row mb-3">
                    <div class="col-2 d-flex align-items-center">
                        <img :src="globalData.STATIC_URL + 'img/icons/headhunter.png'" class="-max-height-32">
                    </div>
                    <div class="col-10">
                        We save you time by finding jobs that are the best fit for you
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col-2 d-flex align-items-center">
                        <img :src="globalData.STATIC_URL + 'img/icons/approved.png'" class="-max-height-32">
                    </div>
                    <div class="col-10">
                        We help you prove yourself by giving you real world projects that will show employers your skills
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col-2 d-flex align-items-center">
                        <img :src="globalData.STATIC_URL + 'img/icons/015-strong.png'" class="-max-height-32">
                    </div>
                    <div class="col-10">
                        We give you the best shot at landing a job through interview prep and summarized data about employers
                    </div>
                </div>
            </div>
        </div>
    </BasePage>
</template>

<script>
import EditUserModal from "../../modals/EditUserModal";
import EmployerRequestInfoModal from "../../modals/EmployerRequestInfoModal";
import BasePage from "../BasePage";

export default {
    name: "SignUpPage",
    components: {BasePage, EditUserModal, EmployerRequestInfoModal},
}
</script>