<template>
    <BaseModal
        :modalId="modalName"
        :modalTitle="(formData.id) ? `Edit role: ${formData.functionName}`: 'Create new role'"
        :primaryButtonText="(formData.id) ? 'Save changes' : 'Create role'"
        :isAllowDelete="Boolean(formData.id)"
        @saveChange="saveChange($event)"
        @deleteObject="deleteObject($event)"
    >
        <div class="mb-3">
            <label for="functionName" class="form-label">Role name</label>
            <input type="text" class="form-control" placeholder="Required" id="functionName" v-model="formData.functionName">
        </div>
    </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal";

export default {
    name: "EditFunctionModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal},
    data() {
        return {
            modalName: 'editFunctionModal',
            crudUrl: 'project-function/',
            isUpdateData: true,
            initDataKey: 'functions',
            requiredFields: {
                functionName: 'functionName',
            },
        }
    },
}
</script>