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
    </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal";
import InputSelectize from "../inputs/InputSelectize";

export default {
    name: "EditSkillModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal, InputSelectize},
    data() {
        return {
            modalName: 'editSkillModal',
            crudUrl: 'project-skill/',
            isHardRefresh: true,
            requiredFields: {
                name: '#skillName',
            },
        }
    },
}
</script>