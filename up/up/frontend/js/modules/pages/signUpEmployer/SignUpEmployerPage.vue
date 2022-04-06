<template>
    <BasePage>
        <div class="row mt-7 mb-3 justify-content-center">
            <div class="col-md-5 card-custom card-custom--shadow">
                <h5 class="fw-bold">
                    Get started with Uprove
                </h5>
                <EmployerRequestInfoModal ref="employerSignUp" :isContentOnly="true"/>
                <button @click="$refs.employerSignUp.saveChange($event)" type="button" class="btn btn-primary w-100 mt-3">
                    {{(initData.isStarter) ? 'Talk to a talent expert' : 'Talk to sales team'}}
                </button>
            </div>
        </div>
    </BasePage>
</template>

<script>
import EmployerRequestInfoModal from "../../modals/EmployerRequestInfoModal";
import BasePage from "../base/BasePage";

export default {
    name: "SignUpEmployerPage",
    components: {BasePage, EmployerRequestInfoModal},
}
</script>