<template>
    <BaseModal
        :modalId="modalName"
        :modalTitle="modalTitle"
        primaryButtonText="Save candidate"
        :isLargeDisplay="true"
        @saveChange="saveChange"
    >
        <div class="mb-3">
            <label class="form-label">
                Jobs to invite candidate to
            </label>
            <InputSelectize
                v-if="employerJobsCfg"
                ref="jobs"
                :elId="getNewElUid()"
                :isParseAsInt="true"
                :cfg="employerJobsCfg"
                @selected="formData.jobs = $event"
            />
        </div>
        <template v-if="formData.jobs">
            <div class="mb-3">
                <InputCheckBox
                    :elId="getNewElUid()"
                    label="Send notification email"
                    :isChecked="true"
                    :isActiveLabel="true"
                    @click="isSendEmail = $event"
                >
                    &nbsp;<InfoToolTip style="display: inline-block" :elId="getNewElUid()" :content="`Sending an email allows you to customize the message to the candidate and increases
                        the chances that they will apply to the position. If unchecked, the candidate will receive an automated notification from Uprove
                        to alert them that they can apply to your company.
                        `"
                    />
                </InputCheckBox>
            </div>
            <div v-if="isSendEmail">
                <div class="mb-3">
                    <label for="fromEmail" class="form-label">From email</label>
                    <input id="fromEmail" type="text" class="form-control" v-model="formData.fromEmail"/>
                </div>
                <div class="mb-3">
                    <label class="form-label">
                        Email
                    </label>
                    <p class="-text-medium">From: {{ formData.fromEmail }}</p>
                    <p class="-text-medium">CC: {{ formData.fromEmail }}</p>
                    <p class="-text-medium">To: {{ formData.email }}</p>
                    <div class="mb-3">
                        <span class="-text-medium">Subject:&nbsp;</span>
                        <input
                            id="emailSubject"
                            type="text" class="form-control"
                            placeholder="Email subject" v-model="emailSubject"
                            style="display: inline-block;"
                        >
                    </div>
                    <InputWsiwyg elId="emailContent" v-model="emailContent"/>
                </div>
            </div>
        </template>
    </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal";
import InfoToolTip from "../components/InfoToolTip";
import InputCheckBox from "../inputs/InputCheckBox";
import InputSelectize from "../inputs/InputSelectize";
import InputWsiwyg from "../inputs/InputWsiwyg";
import employerJobs from "../selectizeCfgs/employerJobs";
import dateUtil from "../../utils/dateUtil";
import dataUtil from "../../utils/data";

export default {
    name: "SaveCandidateModal",
    extends: BaseModal,
    inheritAttrs: false,
    props: ['employerId', 'applications'],
    components: {BaseModal, InfoToolTip, InputCheckBox, InputSelectize, InputWsiwyg},
    data() {
        return {
            modalName: 'saveCandidateModal',
            crudUrl: 'user-job-application/',
            requiredFields: {
                jobs: null  // Set on mounted
            },
            employerJobsCfg: null,
            isSendEmail: true,
            isHardRefresh: true
        }
    },
    computed: {
        candidateName() {
            return `${this.formData.firstName} ${this.formData.lastName}`;
        },
        companyContactName() {
            const user = this.globalData.uproveUser;
            return `${user.firstName} ${user.lastName}`;
        },
        modalTitle() {
            return `Invite ${this.candidateName}`;
        },
        emailSubject() {
            return `New career opportunity with ${this.cData?.employer?.companyName}`;
        },
        emailContent() {
            let jobText = '';
            let additionalText = '';
            const jobCount = this.formData?.jobs?.length;
            if (jobCount) {
                const jobs = this.formData.jobs.map((jobId) => this.cData.jobs.find((j) => j.id === jobId));
                if (jobCount === 1) {
                    const job = jobs[0];
                    jobText = `a new <a href="${this.globalData.BASE_URL}/job-posting/${job.id}/" target="_blank">${job.jobTitle}</a> position.`;
                    additionalText = 'this position';
                } else {
                    jobText = `any of the following ${jobCount} positions: <ul>`;
                    jobs.forEach((job) => {
                        jobText += `<li><a href="${this.globalData.BASE_URL}/job-posting/${job.id}/" target="_blank">${job.jobTitle}</a></li>`;
                    });
                    jobText += '</ul>';
                    additionalText = 'any of these positions';
                }
            }

            return `
                <p>Hi ${this.formData.firstName},</p>
                <p>I reviewed your profile on Uprove and think that you would be a great fit with ${this.cData?.employer?.companyName}
                for ${jobText} You can go to your <a href="${this.globalData.BASE_URL}/candidateDashboard/?tab=applications" target="_blank">Uprove dashboard</a> to view and
                accept my invite to interview for ${additionalText}.
                If you have any questions about ${this.cData?.employer?.companyName}, please email me.</p>
                <p>Sincerely,</p>
                <p>${this.companyContactName}</p>
            `;
        },
    },
    methods: {
        isGoodFormFields(formData) {
            if (this.isSendEmail) {
                if (!this.emailSubject) {
                    this.addPopover($('#emailSubject'), {content: 'An email subject is required', severity: SEVERITY.WARN, isOnce: true});
                    return false;
                }
                if (!this.emailContent) {
                    this.addPopover($('#emailContent'), {content: 'An email body is required', severity: SEVERITY.WARN, isOnce: true});
                    return false;
                }
                if (!formData.fromEmail) {
                    this.addPopover($('#fromEmail'), {content: 'An email address is required', severity: SEVERITY.WARN, isOnce: true});
                    return false;
                }
            }
            return true;
        },
        onModalOpen() {
            // If candidate has applications, filter them out of selection options
            const alreadyAppliedJobIds = (this.formData?.applications?.length) ? this.formData.applications.map((app) => app.jobId) : null;
            this.$refs.jobs.resetOptions(this.cData.jobs.filter((j) => !alreadyAppliedJobIds || !alreadyAppliedJobIds.includes(j.id)));
        },
        readForm() {
            return Object.assign(dataUtil.pick(this.formData, ['email', 'firstName', 'jobs', 'fromEmail', 'defaultProfileId']), {
                userId: this.formData.id,
                isSendEmail: this.isSendEmail,
                emailSubject: this.emailSubject,
                emailContent: this.emailContent,
                status: this.globalData.APPLICATION_STATUS_KEYS.INVITED,
                statusUpdateDateTime: dateUtil.serializeDateTime(dateUtil.now()),
                isInvite: true
            })
        },
        processRawData(rawData) {
            rawData.fromEmail = this.globalData?.uproveUser?.email;
            return rawData;
        }
    },
    async mounted() {
        const alreadyAppliedJobIds = (this.applications?.length) ? this.applications.map((app) => app.jobId) : null;
        this.employerJobsCfg = Object.assign(
            employerJobs.getEmployerJobsCfg(
                this.employerId, {isMulti: true, filterFn: (jobs) => {
                        return jobs.filter((job) => !alreadyAppliedJobIds || !alreadyAppliedJobIds.includes(job.id));
                    }}
            ), {closeAfterSelect: true}
        );
        await this.loadData([
            {route: `account-employer/${this.employerId}/`, dataKey: 'employer'},
            {route: `job-posting/?employerId=${this.employerId}`, dataKey: 'jobs'},
        ]);
    },
    updated() {
        if (this.$refs.jobs) {
            this.requiredFields.jobs = this.$refs.jobs.targetEl;
        }
    }
}
</script>