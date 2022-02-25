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
            <label class="form-label">Evaluation criteria <InfoToolTip :elId="getNewElUid()" :content="infoEvalCriteria"/></label>
            <div>
                <a href="#" @click="toggleAll($event, true)">Select all</a>&nbsp;&nbsp;<a href="#" @click="toggleAll($event, false)">Unselect all</a>
            </div>
            <div v-for="criterion in evaluationCriteria" class="form-check">
                <InputCheckBox
                    :elId="`criterion-${criterion.id}`"
                    :isChecked="criterion.isUsed"
                    :label="criterion.criterion"
                    :isEditable="isEditableCriterion(criterion)"
                    :isEditableTextArea="true"
                    editablePlaceHolder="Add criterion..."
                    @click="criterion.isUsed = !criterion.isUsed"
                    @change="criterion.criterion = $event"
                />
            </div>
            <div class="pt-1">
                <a href="#" @click="addCriterionInput"><i class="fas fa-plus -color-green-text"></i> Add new criterion</a>
            </div>
        </div>
    </BaseModal>
</template>

<script>
import {SEVERITY} from '../../globalData';
import BadgesSkillLevels from "../components/BadgesSkillLevels";
import BadgesSkills from "../components/BadgesSkills";
import BaseModal from "./BaseModal";
import InfoToolTip from "../components/InfoToolTip";
import InputCheckBox from "../inputs/InputCheckBox";
import InputSelectize from "../inputs/InputSelectize";
import dataUtil from "../../utils/data";
import $ from "jquery";

export default {
    name: "EditCustomProjectModal",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BadgesSkillLevels, BadgesSkills, BaseModal, InfoToolTip, InputCheckBox, InputSelectize},
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
            let evalCriteria = (project.evaluationCriteria || []).filter((ec) => !ec.skillLevelBits || ec.skillLevelBits & this.formData.skillLevelBit);
            evalCriteria.forEach((ec) => {
                const existingCriterion = this.initData.customProjectEvaluationCriteria.find((pec) => pec.evaluationCriterionId === ec.id);
                ec.isUsed = dataUtil.isNil(ec.isUsed) ? Boolean(existingCriterion) : ec.isUsed;
            });
            evalCriteria = [...evalCriteria, ...this.formData.newCriterion]
            return dataUtil.sortBy(evalCriteria, ['category', 'isUsed']);
        }
    },
    data() {
        return {
            modalName: 'editCustomProjectModal',
            crudUrl: 'employer-custom-project/',
            isUpdateData: true,
            initDataKey: ['projects', 'customProjectEvaluationCriteria'],
            newCriterionCount: 0,
            infoEvalCriteria: `Check all criteria that evaluators should use when assessing the quality of a candidate's application.`
        }
    },
    methods: {
        isEditableCriterion(criterion) {
            return isNaN(criterion.id) || criterion.employerId;
        },
        processRawData(customProject) {
            this.$refs.linkedJobs.elSel.setValue(customProject.jobs.map((j) => j.id));
            customProject.newCriterion = [];
            return customProject;
        },
        processFormData() {
            const formData = this.readForm();
            formData.employerId = this.initData.employer.id;
            formData.evaluationCriteria = this.evaluationCriteria
            return formData;
        },
        isGoodFormFields(formData) {
            for(let i=0; i<formData.evaluationCriteria.length; i++) {
                const criterion = formData.evaluationCriteria[i];
                if (!criterion.criterion || !criterion.criterion.length) {
                    this.addPopover($(`#criterion-${criterion.id}`).next('textarea'),
                {severity: SEVERITY.WARN, content: 'Required field', isOnce: true}
                    );
                    return false;
                }
            }
            return true;
        },
        addCriterionInput(e) {
            e.preventDefault();
            this.formData.newCriterion.push({
                id: `new-${this.newCriterionCount}`,
                criterion: null,
                category: null,
                isUsed: true,
                skillLevelBits: this.formData.skillLevelBit,
                employerId: this.initData.employer.id
            });
            this.newCriterionCount++;
        },
        toggleAll(e, isUsed) {
            e.preventDefault();
            this.evaluationCriteria.forEach((ec) => { ec.isUsed = isUsed; });
        }
    }
}
</script>