<template>
    <BaseModal
        :modalId="modalName"
        :modalTitle="(formData.id) ? `Edit skill: ${formData.skillName}`: 'Create new skill'"
        :primaryButtonText="(formData.id) ? 'Save changes' : 'Create skill'"
        :isAllowDelete="Boolean(formData.id)"
        @saveChange="saveChange($event)"
        @deleteObject="deleteObject($event)"
    >
        <div class="mb-3">
            <label for="skillName" class="form-label">Skill Name</label>
            <input type="text" class="form-control" placeholder="Required" id="skillName" v-model="formData.skillName">
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

export default {
    name: "EditSkillModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal},
    data() {
        return {
            modalName: 'editSkillModal',
            crudUrl: 'project-skill/',
            isUpdateData: true,
            initDataKey: 'skills',
            requiredFields: {
                skillName: 'skillName',
            },
        }
    },
}
</script>