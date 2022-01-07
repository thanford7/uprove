<template>
    <div class="container-lg">
        <BannerAlert/>
        <div class="row mt-5 mb-3 justify-content-center">
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
    </div>
</template>

<script>
import BannerAlert from "../../components/BannerAlert";
import EditUserModal from "../../modals/EditUserModal";
import EmployerRequestInfoModal from "../../modals/EmployerRequestInfoModal";

export default {
    name: "SignUpPage",
    components: {BannerAlert, EditUserModal, EmployerRequestInfoModal},
}
</script>