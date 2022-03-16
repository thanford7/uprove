<template>
    <BasePage>
        <div v-if="!isMobile" class="row mt-5 mb-3 justify-content-center">
            <div class="col-md-5 card-custom">
                <h4>Candidate Sign Up</h4>
                <EditUserModal ref="userSignUp" :isContentOnly="true"/>
                <button @click="$refs['userSignUp'].saveChange($event)" type="button" class="btn btn-primary w-100">Create account</button>
            </div>
            <div class="col-md-5 card-custom">
                <h4>Employers Get Started</h4>
                <EmployerRequestInfoModal ref="employerRequest" :isContentOnly="true"/>
                <button @click="$refs['employerRequest'].saveChange($event)" type="button" class="btn btn-primary w-100 mt-3">Request demo</button>
            </div>
        </div>
        <div v-else class="mt-3 mb-3">
            <ul class="nav nav-tabs" id="mobileSignUp" role="tablist">
                <li class="nav-item" role="presentation">
                    <button class="nav-link active" id="home-tab" data-bs-toggle="tab" data-bs-target="#mobileEmployerRequest" type="button"
                            role="tab" aria-controls="home" aria-selected="true">Employers
                    </button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="profile-tab" data-bs-toggle="tab" data-bs-target="#mobileCandidateSignUp" type="button"
                            role="tab" aria-controls="profile" aria-selected="false">Candidates
                    </button>
                </li>
            </ul>
            <div class="tab-content" id="myTabContent">
                <div class="tab-pane fade show active" id="mobileEmployerRequest" role="tabpanel" aria-labelledby="home-tab">
                    <EmployerRequestInfoModal ref="employerRequest" :isContentOnly="true"/>
                    <button @click="$refs['employerRequest'].saveChange($event)" type="button" class="btn btn-primary w-100 mt-3">Request demo</button>
                </div>
                <div class="tab-pane fade" id="mobileCandidateSignUp" role="tabpanel" aria-labelledby="profile-tab">
                    <EditUserModal ref="userSignUp" :isContentOnly="true"/>
                    <button @click="$refs['userSignUp'].saveChange($event)" type="button" class="btn btn-primary w-100">Create profile</button>
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