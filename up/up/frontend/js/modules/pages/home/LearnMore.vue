<template>
    <div>
        <BannerAlert/>
        <div class="mb-3 learn-more">
            <InputEmail :elId="getNewElUid()" placeholder="Email" v-model="formData.email"/>
            <button id="lm-reverse-resume" class="btn btn-secondary" :disabled="!formData.email">
                Learn more
            </button>
        </div>
    </div>
</template>

<script>
import InputEmail from "../../inputs/InputEmail";
import BannerAlert from "../../components/BannerAlert";

export default {
    name: "LearnMore",
    props: ['buttonId'],
    components: {BannerAlert, InputEmail},
    data() {
        return {
            crudUrl: 'email/',
        }
    },
    processFormData() {
        const formData = this.readForm();
        formData.type = this.globalData.EMAIL_CANDIDATE_INTEREST;
        formData.subject = 'Candidate interest';
        return formData;
    },
}
</script>