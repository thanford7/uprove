<template>
    <BaseModal
        :modalId="modalName"
        :modalTitle="(formData.id) ? `Edit role: ${formData.name}`: 'Create new role'"
        :primaryButtonText="(formData.id) ? 'Save changes' : 'Create role'"
        :isAllowDelete="Boolean(formData.id)"
        @saveChange="saveChange($event)"
        @deleteObject="deleteObject($event)"
    >
        <div class="mb-3">
            <label for="roleName" class="form-label">Role name</label>
            <input type="text" class="form-control" placeholder="Required" id="roleName" v-model="formData.name">
        </div>
    </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal";

export default {
    name: "EditRoleModal",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal},
    data() {
        return {
            modalName: 'editRoleModal',
            crudUrl: 'project-role/',
            isUpdateData: true,
            initDataKey: 'roles',
            requiredFields: {
                name: 'name',
            },
        }
    },
}
</script>