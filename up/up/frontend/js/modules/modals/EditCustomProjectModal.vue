<template>
    <BaseModal
        :modalId="modalName"
        :modalTitle="`Edit project: ${formData.projectTitle}`"
        primaryButtonText="Save changes"
        :isLargeDisplay="true"
        :isScrollable="true"
        :isAllowDelete="false"
        @saveChange="saveChange($event)"
    >
        <div class="mb-3">
            <label class="form-label">Level & Skills</label>
            <div>
                <BadgesSkillLevels :skillLevels="formData.skillLevel"/>
                <BadgesSkills :skills="formData.skills"/>
            </div>
        </div>
        <div class="mb-3">
            <label for="modalLinkedJobs" class="form-label">Linked jobs</label>
            <InputSelectize
                ref="linkedJobs"
                elId="modalLinkedJobs"
                :isParseAsInt="true"
                placeholder="Required" :cfg="jobsCfg" @selected="formData.linkedJobIds = $event"
            />
        </div>
        <div class="mb-3">
            <label class="form-label">Evaluation criteria</label>
            <div v-if="evaluationCriteria.length" class="-sub-text">Check all that should be included</div>
            <template v-for="criterion in evaluationCriteria">
                <input type="checkbox" class="custom-control-input" :id="`criterion-${criterion.id}`" @click="criterion.isChecked = !criterion.isChecked">
            </template>
            <div class="border-top pt-1">
                <a href="#" @click="addCriterionInput"><i class="fas fa-plus -color-green-text"></i> Add new criterion</a>
            </div>
        </div>
    </BaseModal>
</template>

<script>
import BadgesSkillLevels from "../components/BadgesSkillLevels";
import BadgesSkills from "../components/BadgesSkills";
import BaseModal from "./BaseModal";
import InputSelectize from "../inputs/InputSelectize";
import dataUtil from "../../utils/data";

export default {
    name: "EditCustomProjectModal",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BadgesSkillLevels, BadgesSkills, BaseModal, InputSelectize},
    computed: {
        jobsCfg() {
            const jobs = dataUtil.sortBy(this.initData.employer.jobs.map((job) => ({value: job.id, text: job.jobTitle})), 'text');
            return {
                plugins: ['remove_button'],
                maxItems: null,
                options: jobs
            };
        },
        evaluationCriteria() {
            if (!this.formData.projectId) {
                return [];
            }
            const project = this.initData.projects.find((p) => p.id === this.formData.projectId);
            const evalCriteria = (project.evaluationCriteria || []).filter((ec) => !ec.skillLevelBits || ec.skillLevelBits & this.formData.skillLevelBit);
            evalCriteria.forEach((ec) => {
                const existingCriterion = this.initData.customProjectEvaluationCriteria.find((pec) => pec.evaluationCriterionId === ec.id);
                ec.isUsed = Boolean(existingCriterion);
            });
            return dataUtil.sortBy(evalCriteria, ['category', 'isUsed']);
        }
    },
    data() {
        return {
            modalName: 'editCustomProjectModal',
            crudUrl: 'employer-custom-project/',
            isUpdateData: true,
            initDataKey: 'employer.jobs',
            requiredFields: {
                jobTitle: '#modalJobTitle',
                jobDescription: '#modalJobDescription',
            },
            newCriterionCount: 0
        }
    },
    methods: {
        processRawData(customProject) {
            this.$refs.linkedJobs.elSel.setValue(customProject.jobs.map((j) => j.id));
            this.formData.newCriterion = [];
            return customProject;
        },
        addCriterionInput(e) {
            e.preventDefault();
            this.formData.newCriterion.push({
                id: this.newCriterionCount,
                criterion: null,
                category: null
            });
            this.newCriterionCount++;
        }
    }
}
</script>