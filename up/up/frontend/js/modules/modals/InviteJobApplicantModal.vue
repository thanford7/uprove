<template>
    <BaseModal
        :modalId="modalName"
        modalTitle="Invite job applicants"
        primaryButtonText="Send invites"
        :isLargeDisplay="true"
        :isFooterHidden="true"
        headerSubtext="Copy the suggested instructions below or just the invite link to include in an email to one or more applicants"
    >
        <div class="mb-3">
            <label class="form-label">Suggested instructions
                <i class="fas fa-copy" @click="copyText"></i>
            </label>
            <div id="jobInviteInstructions" class="form-control copy-target">
                We are using Uprove to conduct a project exercise which will evaluate your skills for the
                {{ formData.jobTitle }} position.
                Please use the link below to view the project exercise instructions and submit your project:
                {{ inviteUrl }}
            </div>
        </div>
        <div class="mb-3">
            <label class="form-label">Invite link
                <i class="fas fa-copy" @click="copyText"></i>
            </label>
            <div class="form-control copy-target">
                {{ inviteUrl }}
            </div>
        </div>
    </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal";
import dataUtil from "../../utils/data";

export default {
    name: "InviteJobApplicantModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal},
    data() {
        return {
            modalName: 'inviteJobApplicantModal',
            crudUrl: 'job-invite/',
        }
    },
    computed: {
        inviteUrl() {
            return `${this.globalData.BASE_URL}/job-posting/${this.formData.id}/${this.formData.employerId}/`
        }
    },
    methods: {
        copyText: dataUtil.copyText
    }
}
</script>