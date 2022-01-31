<template>
    <BaseModal
        :modalId="modalName"
        :modalTitle="(formData.id) ? `Edit skill: ${formData.name}`: 'Create new skill'"
        :primaryButtonText="(formData.id) ? 'Save changes' : 'Create skill'"
        :isAllowDelete="Boolean(formData.id)"
        @saveChange="saveChange($event)"
        @deleteObject="deleteObject($event)"
    >
        <div class="mb-3">
            <label for="skillName" class="form-label">Skill Name</label>
            <input type="text" class="form-control" placeholder="Required" id="skillName" v-model="formData.name">
        </div>
        <div class="mb-3">
            <label for="skillInstruction" class="form-label">Skill Instruction</label>
            <textarea
                rows="3" class="form-control"
                placeholder="Optional"
                id="skillInstruction"
                v-model="formData.instruction"
            />
        </div>
        <div class="mb-3">
            <label for="modalSkillPriority" class="form-label">Priority</label>
            <InputSelectize
                ref="skillPriority"
                elId="modalSkillPriority"
                :cfg="skillPriorityCfg"
                @selected="setSkillPriority"
            />
        </div>
    </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal";
import InputSelectize from "../inputs/InputSelectize";
import skillPrioritySelectize from "../selectizeCfgs/skillPriority";

export default {
    name: "EditSkillModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal, InputSelectize},
    data() {
        return {
            modalName: 'editSkillModal',
            crudUrl: 'project-skill/',
            isUpdateData: true,
            initDataKey: 'skills',
            requiredFields: {
                name: '#skillName',
            },
            skillPriorityCfg: skillPrioritySelectize.cfg
        }
    },
    methods: {
        setFormFields() {
            this.$refs.skillPriority.elSel.setValue(skillPrioritySelectize.getPriorityLabel(this.formData));
        },
        setSkillPriority(val) {
            skillPrioritySelectize.setSkillPriority(val, this.formData);
        }
    }
}
</script>