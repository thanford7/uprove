<template>
    <BaseModal
        :modalId="modalName"
        modalTitle="Request information"
        headerSubtext="Once you submit the form, we'll email you additional information and find a time to demo the platform"
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
        <div class="mb-3">
            <label for="formEmployerRequestTitle" class="form-label">Your Title</label>
            <input type="text" class="form-control" placeholder="Required" id="formEmployerRequestTitle" v-model="formData.title">
        </div>
        <div class="mb-3">
            <label for="formEmployerRequestCoSize" class="form-label">Company Employee Count</label>
            <InputSelectize
                ref="sel1"
                elId="formEmployerRequestCoSize"
                placeholder="Optional" :cfg="coSizeCfg" @selected="formData.size = $event"/>
        </div>
        <div class="mb-3">
            <label for="formEmployerRequestFunctions" class="form-label">Functions You're Hiring</label>
            <InputSelectize
                ref="sel2"
                elId="formEmployerRequestFunctions"
                placeholder="Optional" :cfg="functionsCfg" @selected="formData.roleFunctions = $event"/>
        </div>
        <div>
            <label for="formEmployerRequestSkills" class="form-label">Skills You're Hiring</label>
            <InputSelectize
                ref="sel3"
                elId="formEmployerRequestSkills"
                placeholder="Optional" :cfg="skillsCfg" @selected="formData.roleSkills = $event"/>
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
import BaseModal from './BaseModal.vue';
import dataUtil from '../../utils/data';
import InputEmail from '../inputs/InputEmail';
import InputSelectize from '../inputs/InputSelectize';
import FormChecker from '../../utils/form';

export default {
    name: "EmployerRequestInfoModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal, InputEmail, InputSelectize},
    data() {
        return {
            modalName: 'employerRequestInfoModal',
            crudUrl: 'email/',
            coSizeCfg: {
                maxItems: 1,
                options: [
                    {value: '1-10', text: '1-10'},
                    {value: '11-50', text: '11-50'},
                    {value: '51-100', text: '51-100'},
                    {value: '101-250', text: '101-250'},
                    {value: '251-500', text: '251-500'},
                    {value: '501-1000', text: '501-1000'},
                    {value: '1001+', text: '1001+'},
                ]
            },
            requiredFields: {
                firstName: 'formEmployerRequestFName',
                lastName: 'formEmployerRequestLName',
                companyName: 'formEmployerRequestCName',
                fromEmail: 'formEmployerRequestEmail',
                title: 'formEmployerRequestTitle'
            }
        }
    },
    computed: {
        functionsCfg() {
            return {
                plugins: ['remove_button'],
                maxItems: null,
                options: dataUtil.sortBy(this.initData.functions.map((f) => ({value: f.id, text: f.functionName})), 'text')
            }
        },
        skillsCfg() {
            return {
                plugins: ['remove_button'],
                maxItems: null,
                options: dataUtil.sortBy(this.initData.skills.map((s) => ({value: s.id, text: s.skillName})), 'text')
            }
        }
    },
    methods: {
        readForm() {
            return {
                ...this.formData,
                type: this.globalData.EMAIL_EMPLOYER_INTEREST,
                subject: 'Employer interest'
            };
        },
        isGoodFormFields(formData) {
            if (!FormChecker.isGoodEmail(formData.fromEmail)) {
                this.addPopover($('#formEmployerRequestEmail'), {content: 'Please add valid email', isOnce: true});
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