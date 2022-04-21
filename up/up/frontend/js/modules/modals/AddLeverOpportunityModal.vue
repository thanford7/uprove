<template>
    <BaseModal
        v-if="employerJobsCfg"
        :modalId="modalName"
        :modalTitle="modalTitle"
        :isLargeDisplay="true"
        primaryButtonText="Add to Lever"
        @saveChange="saveChange"
    >
        <div class="mb-3">
            <label class="form-label">
                Job to add candidate to
                <InfoToolTip :elId="getNewElUid()" :content="`This will add the candidate to your Lever account in the 'New Lead' stage`"/>
            </label>
            <InputSelectize
                ref="jobs"
                :elId="getNewElUid()"
                :isParseAsInt="true"
                :cfg="employerJobsCfg"
                @selected="setLeverOpportunity($event)"
            />
        </div>
        <div class="mb-3">
            <label class="form-label">
                Note
                <InfoToolTip :elId="getNewElUid()" content="This note will be added to the opportunity in Lever"/>
            </label>
            <textarea
                rows="3" class="form-control"
                placeholder="Add a note"
                v-model="formData.note"
            />
        </div>
    </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal";
import employerJobs from "../selectizeCfgs/employerJobs";
import InfoToolTip from "../components/InfoToolTip";
import InputSelectize from "../inputs/InputSelectize";

export default {
    extends: BaseModal,
    inheritAttrs: false,
    name: "AddLeverOpportunityModal",
    components: {InfoToolTip, BaseModal, InputSelectize},
    props: ['employerId'],
    computed: {
        candidateName() {
            return `${this.formData.firstName} ${this.formData.lastName}`;
        },
        modalTitle() {
            return `Add ${this.candidateName} as new Lever opportunity`;
        }
    },
    data() {
        return {
            modalName: 'addLeverOpportunityModal',
            crudUrl: null,
            employerJobsCfg: null,
            requiredFields: {
                leverPostingKey: null
            }
        }
    },
    methods: {
        getAjaxCfgOverride() {
            return {method: 'POST'};
        },
        setLeverOpportunity(jobId) {
            const job = this.$refs.jobs.elSel.options[jobId];
            this.formData.jobId = jobId;
            this.formData.leverPostingKey = job.leverPostingKey;
        }
    },
    mounted() {
        this.crudUrl = `lever/opportunities/${this.employerId}/`;
        this.employerJobsCfg = employerJobs.getEmployerJobsCfg(
            this.employerId,
            {filterFn: (jobs) => jobs.filter((j) => j.leverPostingKey)}
        );
    },
    updated() {
        if (this.$refs.jobs) {
            this.requiredFields.leverPostingKey = this.$refs.jobs.targetEl;
        }
    }
}
</script>