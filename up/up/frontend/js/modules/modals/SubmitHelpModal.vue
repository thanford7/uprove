<template>
    <BaseModal
        :isContentOnly="isContentOnly"
        :modalId="modalName"
        primaryButtonText="Submit"
        @saveChange="saveChange($event, true)"
    >
        <template v-if="!isLoggedIn">
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
        </template>
        <div class="mb-3">
            <label class="form-label" for="contactMessage">Message</label>
            <textarea
                rows="3" class="form-control"
                placeholder="Tell us how we can help..."
                id="contactMessage"
                v-model="formData.message"
            />
        </div>
    </BaseModal>
</template>

<script>
import {severity} from "../../vueMixins";
import BaseModal from "./BaseModal";
import FormChecker from "../../utils/form";
import globalData from "../../globalData";
import InputEmail from "../inputs/InputEmail";

export default {
    name: "SubmitHelpModal",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal, InputEmail},
    props: ['isContentOnly'],
    data() {
        return {
            modalName: 'submitHelpModal',
            crudUrl: 'email/',
            requiredFields: {
                message: '#contactMessage'
            }
        }
    },
    methods: {
        isGoodFormFields(formData) {
            if (!this.isLoggedIn) {
                if (!FormChecker.isGoodEmail(formData.fromEmail)) {
                    this.addPopover($('#contactEmail'), {content: 'Please add valid email', isOnce: true, severity: severity.WARN});
                    return false;
                }
                if (!formData.name) {
                    this.addPopover($('#contactName'), {content: 'Required field', isOnce: true, severity: severity.WARN});
                    return false;
                }
            }
            return true;
        },
        processFormData() {
            const formData = this.readForm();
            formData.type = this.globalData.EMAIL_CONTACT;
            formData.subject = 'User contact';

            if (this.isLoggedIn) {
                const user = globalData.uproveUser;
                formData.fromEmail = user.email;
                formData.name = `${user.firstName} ${user.lastName}`;
            }
            return formData;
        },
        getAjaxCfgOverride() {
            return {method: 'POST'};
        },
        getSuccessMessage(data) {
            return 'Email sent successfully';
        },
        getFailureMessage(errorThrown) {
            return `Email failed: ${errorThrown}`;
        }
    }
}
</script>