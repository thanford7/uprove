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
                <font-awesome-icon :icon="['fas', 'copy']" @click="copyText"/>
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
                <font-awesome-icon :icon="['fas', 'copy']" @click="copyText"/>
            </label>
            <div class="form-control copy-target">
                {{ inviteUrl }}
            </div>
        </div>
    </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal";

export default {
    name: "InviteJobApplicantModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal},
    data() {
        return {
            modalName: 'inviteJobApplicantModal',
            crudUrl: 'job-invite/',  // Not implemented yet - will add for option to email directly from app
        }
    },
    computed: {
        inviteUrl() {
            return `www.uprove.co/job-posting/${this.formData.id}/`
        }
    },
    methods: {
        copyText(e) {
            const target$ = $(e.currentTarget);
            const text = target$.closest('div').find('.copy-target').text();
            const copyMsgId = this.getNewElUid();
            navigator.clipboard.writeText(text).then(
                () => {
                    target$.closest('label').append(`<span id="${copyMsgId}" class="-color-green-text -sub-text"> Copied successfully</span>`)
                }, () => {
                    target$.closest('label').append('<span id="${copyMsgId}" class="-color-red-text -sub-text"> Copy failed. Please copy manually</span>')
                }
            );
            setTimeout(() => {
                $(`#${copyMsgId}`).remove()
            }, 3000);
        }
    }
}
</script>