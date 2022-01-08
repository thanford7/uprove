<template>
    <BaseModal
        :modalId="modalName"
        primaryButtonText="Sign in"
        @saveChange="saveChange($event, true)"
    >
        <div class="mb-3">
            <label for="signInEmail" class="form-label">Email</label>
            <InputEmail elId="signInEmail" placeholder="myemail@gmail.com" v-model="formData.email"/>
        </div>
        <div class="mb-3">
            <label for="signInPassword" class="form-label">Password</label>
            <input type="password" class="form-control" placeholder="Required" id="signInPassword" v-model="formData.password">
        </div>
        <div>
            <a href="#" @click="eventBus.emit('open:resetPasswordModal')" data-bs-dismiss="modal">Forgot password?</a>
        </div>
    </BaseModal>
</template>

<script>
import {severity} from "../../vueMixins";
import BaseModal from "./BaseModal";
import InputEmail from "../inputs/InputEmail";
import FormChecker from "../../utils/form";

export default {
    name: "SignInModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal, InputEmail},
    data() {
        return {
            modalName: 'signInModal',
            crudUrl: 'login/',
            requiredFields: {
                email: 'signInEmail',
                password: 'signInPassword'
            }
        }
    },
    methods: {
        isGoodFormFields(formData) {
            if (!FormChecker.isGoodEmail(formData.email)) {
                this.addPopover($('#signInEmail'), {content: 'Please use valid email', severity: severity.WARN, isOnce: true});
                return false;
            }
            return true;
        },
        processFormData(rawData) {
            const data = this.readForm();
            const redirect = window.location.pathname;
            if (!redirect.includes('sign-up')) {
                data.redirect =redirect;
            }
            return data;
        }
    }
}
</script>