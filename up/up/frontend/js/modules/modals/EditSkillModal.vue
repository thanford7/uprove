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
            <label for="skillName" class="form-label">Skill name</label>
            <input type="text" class="form-control" placeholder="Required" id="skillName" v-model="formData.skillName">
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
            requiredFields: {
                skillName: 'skillName',
            },
        }
    },
}
</script>