<template>
    <div class="learn-more">
        <BannerAlert/>
        <div class="input-group mb-3">
            <InputEmail ref="email" :elId="getNewElUid()" placeholder="Email" v-model="formData.email"/>
            <button id="lm-reverse-resume" class="btn btn-secondary btn-sm" @click="saveChange">
                <i class="fas fa-paper-plane"></i>
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
    props: ['buttonId', 'interestType'],
    components: {BannerAlert, InputEmail},
    data() {
        return {
            crudUrl: 'email/',
            requiredFields: {
                email: null // Set on mounted
            }
        }
    },
    methods: {
        getAjaxCfgOverride() {
            return {method: 'POST'};
        },
        getSuccessMessage() {
            return 'Email sent to our candidate advocate team. We will respond shortly. Thanks for your interest!'
        },
        processFormData() {
            const formData = this.readForm();
            formData.type = this.globalData.EMAIL_CANDIDATE_INTEREST;
            formData.subject = 'Candidate interest';
            formData.interestType = this.interestType;
            return formData;
        },
    },
    mounted() {
        this.requiredFields.email = `#${this.$refs.email.elId}`;
    }
}
</script>