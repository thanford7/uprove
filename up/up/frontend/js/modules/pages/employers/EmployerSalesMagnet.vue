<template>
    <div id="employerMagnet" class="d-flex justify-content-end">
        <div class="col-md-6 card-custom">
            <div class="float-end">
                <i class="fas fa-times fa-lg" @click="$emit('close')"></i>
            </div>
            <div class="image-wrap d-flex align-items-center">
                <img :src="globalData.STATIC_URL + 'img/icons/029-skill.png'">
                <h5 class="d-inline ms-2">Want to use skill assessments in your hiring process?</h5>
            </div>
            <div class="row mt-2">
                <div class="col-md-4">
                    <img :src="globalData.MEDIA_URL + 'SalesMagnetThumbnail.png'" style="max-height: 200px;">
                </div>
                <div class="col-md-8 ps-md-0 pt-md-0 pt-2">
                    <ListFontAwesome
                        faClassesStr="fas fa-check-circle"
                        faColor="green"
                        :items="[
                            'Discover hidden talent',
                            'Avoid bad hires',
                            'Reduce bias'
                        ]"
                    />
                </div>
            </div>
            <div class="mt-3 mb-3 -text-bold">Enter your contact info to download the guide</div>
            <EmployerRequestInfoModal
                ref="magnetSignUp"
                :isContentOnly="true"
                :isExcludeNote="true"
                :isExcludeEmail="true"
                :successFn="downloadMagnet"
            />
            <button @click="$refs.magnetSignUp.saveChange" type="button" class="btn btn-primary w-100 mt-2">
                <i class="fas fa-download"></i> Download guide
            </button>
        </div>
    </div>
</template>

<script>
import EmployerRequestInfoModal from "../../modals/EmployerRequestInfoModal";
import InputEmail from "../../inputs/InputEmail";
import ListFontAwesome from "../../components/ListFontAwesome";

export default {
    name: "EmployerSalesMagnet",
    components: {EmployerRequestInfoModal, InputEmail, ListFontAwesome},
    methods: {
        downloadMagnet() {
            this.$emit('close');
            window.open(this.globalData.MEDIA_URL + 'Uprove - Leveraging Skill Assessments to Improve Hiring.pdf', '_blank');
        }
    }
}
</script>