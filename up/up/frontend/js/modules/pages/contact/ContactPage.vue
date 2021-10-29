<template>
    <div id="vue-container" class="container-fluid">
        <BannerAlert :alerts="alerts"/>
        <div class="row mt-3 mb-3">
            <h2>Contact us</h2>
            <div class="col-md-6 pt-3 call-out-box" :class="(isMobile) ? 'mb-3' : ''">
                <component :is="(isMobile) ? 'h6' : 'h2'">We want you to have a fantastic hiring experience.</component>
                <font-awesome-icon :icon="['fas', 'chart-line']" :size="(isMobile) ? '2x' : '10x'"/>
                <component :is="(isMobile) ? 'h6' : 'h2'">Connect with one of our project experts to see how we can help.</component>
            </div>
            <div class="col-md-6">
                <form>
                    <div class="mb-3">
                        <label for="contactEmail" class="form-label">Email address</label>
                        <InputEmail elId="contactEmail" placeholder="Required" v-model="formData.fromEmail"/>
                    </div>
                    <div class="mb-3">
                        <label for="contactName" class="form-label">Name</label>
                        <input type="text" class="form-control" id="contactName" placeholder="Required" v-model="formData.name">
                    </div>
                    <div class="mb-3">
                        <label for="contactCompany" class="form-label">Company</label>
                        <input type="text" class="form-control" id="contactCompany" placeholder="Leave blank if you are not an employer" v-model="formData.company">
                    </div>
                    <div class="mb-3">
                        <label class="form-label" for="contactMessage">Message</label>
                        <textarea
                            rows="3" class="form-control"
                            placeholder="Tell us how we can help..."
                            id="contactMessage"
                            v-model="formData.message"
                        />
                    </div>
                    <button type="submit" class="btn btn-primary" @click="saveChange">Send message</button>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import {mapState} from 'vuex';
import BannerAlert from "../../components/BannerAlert";
import InputEmail from "../../inputs/InputEmail";
import mainData from "../../../mainData";

export default {
    name: 'ContactPage.vue',
    components: {
        BannerAlert,
        InputEmail
    },
    computed: mapState({
        eventBus: 'eventBus',
        isMobile: 'isMobile'
    }),
    data() {
        return {
            baseUrl: '/api/v1/',
            crudUrl: 'email/',
            formData: {},
            alerts: []
        }
    },
    methods: {
        readForm() {
            return {
                ...this.formData,
                type: mainData.EMAIL_CONTACT,
                subject: 'Email from contact page'
            };
        },
        processFormData(formData) {
            return formData;
        },
        isGoodFormData(formData) {
            const {fromEmail, name, message} = formData;
            if (!fromEmail) {
                // TODO: Add popover, add regex for email
                return false;
            }
            if (!name) {
                return false;
            }
            if (!message) {
                return false;
            }
        },
        saveChange(e) {
            e.preventDefault();
            this.superSaveChange({method: 'POST'});
            this.formData = {};
        },
        onSaveSuccess() {
            this.alerts.push({
                message: 'Email sent successfully',
                alertType: 'success'
            });
        },
        onSaveFailure(xhr, textStatus, errorThrown) {
            this.alerts.push({
                message: `Email failed: ${errorThrown}`,
                alertType: 'danger'
            });
        },
        superSaveChange(cfg = {}) {
            const formData = this.readForm();
            const requestData = this.processFormData(formData);
            if(!this.isGoodFormData(formData)) {
                return;
            }

            $.ajax(Object.assign({
                url: this.baseUrl + this.crudUrl,
                method: 'PUT',
                data: JSON.stringify(requestData),
                contentType: 'application/json',
                success: this.onSaveSuccess,
                error: this.onSaveFailure
            }, cfg));
        },

    },
}
</script>