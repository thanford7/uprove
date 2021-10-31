<template>
    <div>
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
import BannerAlert from "../../components/BannerAlert";
import FormChecker from "../../../utils/form";
import InputEmail from "../../inputs/InputEmail";

export default {
    name: 'ContactPage.vue',
    components: {
        BannerAlert,
        InputEmail
    },
    data() {
        return {
            crudUrl: 'email/',
            requiredFields: {
                fromEmail: 'contactEmail',
                name: 'contactName',
                message: 'contactMessage'
            }
        }
    },
    methods: {
        readForm() {
            return {
                ...this.formData,
                type: this.globalData.EMAIL_CONTACT,
                subject: 'Email from contact page'
            };
        },
        isGoodFormFields(formData) {
            if (!FormChecker.isGoodEmail(formData.fromEmail)) {
                this.addPopover($('#contactEmail'), {content: 'Please add valid email', isOnce: true});
                return false;
            }
            return true;
        },
        getAjaxCfgOverride() {
            return {method: 'POST'};
        },
    },
    mounted() {
        this.eventBus.on('ajaxSuccess', () => {
            this.alerts.push({
                message: 'Email sent successfully',
                alertType: 'success'
            });
        });
        this.eventBus.on('ajaxFailure', ({xhr, textStatus, errorThrown}) => {
            this.alerts.push({
                message: `Email failed: ${errorThrown}`,
                alertType: 'danger'
            });
        });
    }
}
</script>