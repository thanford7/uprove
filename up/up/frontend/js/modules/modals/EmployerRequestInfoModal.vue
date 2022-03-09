<template>
    <BaseModal
        :isContentOnly="isContentOnly"
        :modalId="modalName"
        modalTitle="Request information"
        primaryButtonText="Send me info"
        @saveChange="saveChange"
    >
        <div class="mb-3">
            <label for="formEmployerRequestFName" class="form-label">First Name</label>
            <input type="text" class="form-control" placeholder="Required" id="formEmployerRequestFName" v-model="formData.firstName">
        </div>
        <div class="mb-3">
            <label for="formEmployerRequestLName" class="form-label">Last Name</label>
            <input type="text" class="form-control" placeholder="Required" id="formEmployerRequestLName" v-model="formData.lastName">
        </div>
        <div class="mb-3">
            <label for="formEmployerRequestCName" class="form-label">Company Name</label>
            <input type="text" class="form-control" placeholder="Required" id="formEmployerRequestCName" v-model="formData.companyName">
        </div>
        <div class="mb-3">
            <label for="formEmployerRequestEmail" class="form-label">Email</label>
            <InputEmail elId="formEmployerRequestEmail" placeholder="Required" v-model="formData.fromEmail"/>
        </div>
        <div>
            <label for="formEmployerRequestNote" class="form-label">Note</label>
            <textarea
                rows="3" class="form-control"
                placeholder="Any other questions or information you want to share..."
                id="formEmployerRequestNote"
                v-model="formData.note"
            />
        </div>
    </BaseModal>
</template>

<script>
import {SEVERITY} from '../../globalData';
import BaseModal from './BaseModal.vue';
import InputEmail from '../inputs/InputEmail';
import InputSelectize from '../inputs/InputSelectize';
import FormChecker from '../../utils/form';

export default {
    name: "EmployerRequestInfoModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    props: ['isContentOnly'],
    components: {BaseModal, InputEmail, InputSelectize},
    data() {
        return {
            modalName: 'employerRequestInfoModal',
            crudUrl: 'email/',
            requiredFields: {
                firstName: '#formEmployerRequestFName',
                lastName: '#formEmployerRequestLName',
                companyName: '#formEmployerRequestCName',
                fromEmail: '#formEmployerRequestEmail'
            }
        }
    },
    methods: {
        readForm() {
            return {
                ...this.formData,
                type: this.globalData.EMAIL_EMPLOYER_INTEREST,
            };
        },
        isGoodFormFields(formData) {
            if (!FormChecker.isGoodEmail(formData.fromEmail)) {
                this.addPopover(
                    $('#formEmployerRequestEmail'),
                    {content: 'Please add valid email', severity: SEVERITY.WARN, isOnce: true}
                );
                return false;
            }
            return true;
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