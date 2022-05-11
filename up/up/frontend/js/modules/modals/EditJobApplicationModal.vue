<template>
    <BaseModal
        :modalId="modalName"
        :modalTitle="(formData.id) ? `Edit application: ${formData.job.employer} - ${formData.job.jobTitle}`: 'Create new application'"
        :primaryButtonText="(formData.id) ? 'Save changes' : 'Create application'"
        @saveChange="saveChange($event)"
        @deleteObject="deleteObject($event)"
    >
        <div class="mb-3">
            <label class="form-label">Project to Submit</label>
            <InputSelectize
                ref="applicationProject"
                elId="applicationProject"
                placeholder="Required"
                :cfg="{
                    maxItems: 1,
                    valueField: 'id',
                    labelField: 'projectTitle'
                }"
                @selected="formData.userProjectId = $event"
            />
            <div v-if="!isProjectAllowed" class="-sub-text">
                <i class="fas fa-exclamation-triangle -color-yellow-text"></i> This project is no longer accepted for this job.
                You can still submit it and the employer will review it, however, if you change your project to submit, you
                will no longer be able to use the current project for submission.
            </div>
        </div>
        <template v-slot:footer>
            <button v-if="isShowWithdraw" type="button" class="btn btn-danger" @click="withdrawApp">Withdraw application</button>
            <button v-if="isShowSubmit" @click="submitApp" type="button" class="btn btn-primary">Submit application</button>
        </template>
    </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal";
import InputSelectize from "../inputs/InputSelectize";
import dateUtil from "../../utils/dateUtil";
import dayjs from "dayjs/esm";
import dataUtil from "../../utils/data";

export default {
    name: "EditJobApplicationModal",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal, InputSelectize},
    data() {
        return {
            modalName: 'editJobApplicationModal',
            crudUrl: 'user-job-application/',
            isHardRefresh: true,
            requiredFields: {
                userProjectId: null,
            },
            allowedProjectIds: null
        }
    },
    computed: {
        isProjectAllowed() {
            if (!this.formData.userProjectId) {
                return false;
            }
            const userProject = this.initData.userProjects.find((up) => up.id === this.formData.userProjectId);
            if (!userProject) {
                return false;
            }
            return this.allowedProjectIds.includes(userProject.customProject.id);
        },
        isShowWithdraw() {
            return !this.formData.withdrawDateTime && this.formData.submissionDateTime;
        },
        isShowSubmit() {
            return !this.formData.submissionDateTime && !(this.formData.declineDateTime || this.formData.approveDateTime);
        }
    },
    methods: {
        processFormData() {
            return Object.assign(
                {userId: this.initData.user.id},
                dataUtil.pick(this.formData, ['id', 'userProjectId', 'submissionDateTime', 'withdrawDateTime'])
            );
        },
        processRawData(applicationData) {
            this.allowedProjectIds = applicationData.job.allowedProjects.map((ap) => ap.id);

            // Set project application options
            this.$refs.applicationProject.resetOptions(applicationData.job.allowedProjects)

            // Set currently selected project
            this.$refs.applicationProject.elSel.setValue(applicationData?.customProject?.id);

            return applicationData;
        },
        submitApp (e) {
            this.formData.submissionDateTime = dateUtil.serializeDateTime(dayjs());
            this.formData.withdrawDateTime = null;
            this.saveChange(e);
        },
        withdrawApp(e) {
            this.formData.submissionDateTime = null;
            this.formData.withdrawDateTime = dateUtil.serializeDateTime(dayjs());
            this.saveChange(e);
        }
    },
    mounted() {
        // Update field checking
        this.userProjectId = this.$refs.applicationProject.targetEl;
    }
}
</script>