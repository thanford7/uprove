<template>
    <BaseModal
        :modalId="modalName"
        modalTitle="Request account"
        headerSubtext="We will review your information and send you an approval decision within 24 hours"
        primaryButtonText="Request account"
        @saveChange="saveChange"
    >
        <div class="mb-3">
            <label for="formCandidateRequestFName" class="form-label">First Name</label>
            <input type="text" class="form-control" placeholder="Required" id="formCandidateRequestFName" v-model="formData.firstName">
        </div>
        <div class="mb-3">
            <label for="formCandidateRequestLName" class="form-label">Last Name</label>
            <input type="text" class="form-control" placeholder="Required" id="formCandidateRequestLName" v-model="formData.lastName">
        </div>
        <div class="mb-3">
            <label for="formCandidateRequestEmail" class="form-label">Email</label>
            <InputEmail elId="formCandidateRequestEmail" placeholder="Required" v-model="formData.fromEmail"/>
        </div>
        <div class="mb-3">
            <label for="formCandidateLinkedIn" class="form-label">LinkedIn Profile Link</label>
            <input type="text" class="form-control" placeholder="Required" id="formCandidateLinkedIn" v-model="formData.linkedInLink">
        </div>
        <div class="mb-3">
            <label for="formCandidateReferrer" class="form-label">Referral</label>
            <input type="text" class="form-control" placeholder="Optional: First and last name of person that referred you" id="formCandidateReferrer" v-model="formData.referrer">
        </div>
        <div class="mb-3">
            <label for="formCandidateFunctions" class="form-label">Positions of Interest</label>
            <InputSelectize
                ref="sel1"
                elId="formCandidateFunctions"
                placeholder="Optional" :cfg="functionsCfg" @selected="formData.roleFunctions = $event"/>
        </div>
        <div>
            <label for="formCandidateSkills" class="form-label">Skills You Have</label>
            <InputSelectize
                ref="sel2"
                elId="formCandidateSkills"
                placeholder="Optional" :cfg="skillsCfg" @selected="formData.roleSkills = $event"/>
        </div>
        <div>
            <label for="formCandidateNote" class="form-label">Note</label>
            <textarea
                rows="3" class="form-control"
                placeholder="Any other questions or information you want to share..."
                id="formCandidateNote"
                v-model="formData.note"
            />
        </div>
    </BaseModal>
</template>
import BaseModal from './BaseModal.vue';
import InputEmail from "../inputs/InputEmail";
import InputSelectize from "../inputs/InputSelectize";
import FormChecker from "../../utils/form";

<script>
import BaseModal from "./BaseModal";
import InputEmail from "../inputs/InputEmail";
import InputSelectize from "../inputs/InputSelectize";
import FormChecker from "../../utils/form";

export default {
    name: "CandidateRequestAccountModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal, InputEmail, InputSelectize},
    data() {
        return {
            modalName: 'candidateRequestAccountModal',
            crudUrl: 'email/',
            requiredFields: {
                firstName: 'formCandidateRequestFName',
                lastName: 'formCandidateRequestLName',
                fromEmail: 'formCandidateRequestEmail',
                linkedInLink: 'formCandidateLinkedIn',
            }
        }
    },
    computed: {
        functionsCfg() {
            return {
                plugins: ['remove_button'],
                maxItems: null,
                options: _.sortBy(this.initData.functions.map((f) => ({value: f.id, text: f.functionName})), ['text'])
            }
        },
        skillsCfg() {
            return {
                plugins: ['remove_button'],
                maxItems: null,
                options: _.sortBy(this.initData.skills.map((s) => ({value: s.id, text: s.skillName})), ['text'])
            }
        }
    },
    methods: {
        readForm() {
            return {
                ...this.formData,
                type: this.globalData.EMAIL_CANDIDATE_INTEREST,
                subject: 'Candidate interest'
            };
        },
        clearFormData() {
            ['sel1', 'sel2'].forEach((selRef) => {
                const sel = this.$refs[selRef];
                sel.elSel.clear(true);
            });
        },
        isGoodFormFields(formData) {
            if (!FormChecker.isGoodEmail(formData.fromEmail)) {
                this.addPopover($('#formCandidateRequestEmail'), {content: 'Please add valid email', isOnce: true});
                return false;
            }
            if (!FormChecker.isGoodWebLink(formData.linkedInLink) || !formData.linkedInLink.toLowerCase().includes('linkedin.com')) {
                this.addPopover($('#formCandidateLinkedIn'), {
                    content: 'Please add valid LinkedIn profile address. Example: www.linkedin.com/in/<your profile>/',
                    isOnce: true
                });
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