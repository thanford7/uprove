<template>
    <BaseModal
        :modalId="modalName"
        primaryButtonText="Email password reset"
        @saveChange="saveChange($event, true)"
    >
        <div class="mb-3">
            <label for="resetEmail" class="form-label">Email</label>
            <InputEmail elId="resetEmail" placeholder="myemail@gmail.com" v-model="formData.email"/>
        </div>
    </BaseModal>
</template>

<script>
import {severity} from "../../vueMixins";
import BaseModal from "./BaseModal";
import InputEmail from "../inputs/InputEmail";
import FormChecker from "../../utils/form";

export default {
    name: "ResetPasswordModal",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal, InputEmail},
    data() {
        return {
            modalName: 'resetPasswordModal',
            crudUrl: 'password-reset-generate/',
            successAlertType: severity.INFO,
            requiredFields: {
                email: 'resetEmail',
            }
        }
    },
    methods: {
        isGoodFormFields(formData) {
            if (!FormChecker.isGoodEmail(formData.email)) {
                this.addPopover($('#resetEmail'), {content: 'Please use valid email', severity: severity.WARN, isOnce: true});
                return false;
            }
            return true;
        },
        getSuccessMessage(email) {
            return `Reset password email sent to ${email}`;
        }
    }
}
</script>

<style scoped>

</style>