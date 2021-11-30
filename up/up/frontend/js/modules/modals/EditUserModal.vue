<template>
    <BaseModal
        :modalId="modalName"
        :modalTitle="(formData.id) ? `Edit user: ${formData.firstName} ${formData.lastName} (${formData.id})`: 'Create new user'"
        :primaryButtonText="(formData.id) ? 'Save changes' : 'Create user'"
        :isAllowDelete="Boolean(formData.id)"
        @saveChange="saveChange($event)"
        @deleteObject="deleteObject($event)"
    >
        <div class="mb-3">
            <label for="userFName" class="form-label">First name</label>
            <input type="text" class="form-control" placeholder="Required" id="userFName" v-model="formData.firstName">
        </div>
        <div class="mb-3">
            <label for="userFName" class="form-label">Middle name</label>
            <input type="text" class="form-control" placeholder="Optional" id="userMName" v-model="formData.middleName">
        </div>
        <div class="mb-3">
            <label for="userFName" class="form-label">Last name</label>
            <input type="text" class="form-control" placeholder="Required" id="userLName" v-model="formData.lastName">
        </div>
        <div class="mb-3">
            <label for="birthDate" class="form-label">Birth Date</label>
            <input type="date" class="form-control" placeholder="Optional" id="birthDate" v-model="formData.birthDate">
        </div>
        <div class="mb-3">
            <label for="userEmail" class="form-label">Email</label>
            <InputEmail elId="userEmail" placeholder="Required" v-model="formData.email"/>
        </div>
        <div class="mb-3">
            <label for="userTypes" class="form-label">User Types</label>
            <InputSelectize
                ref="userTypes"
                elId="userTypes"
                :isParseAsInt="true"
                placeholder="Required" :cfg="userTypesCfg" @selected="formData.userTypes = $event"
            />
        </div>
        <template v-if="globalData.uproveUser && globalData.uproveUser.isSuperUser">
            <div class="mb-3">
                <div class="custom-control custom-checkbox">
                    <input type="checkbox" class="custom-control-input" id="userIsStaff" v-model="formData.isStaff">
                    &nbsp;<label class="custom-control-label" for="userIsStaff">Is Staff</label>
                </div>
            </div>
            <div class="mb-3">
                <div class="custom-control custom-checkbox">
                    <input type="checkbox" class="custom-control-input" id="userIsSuperUser"
                           v-model="formData.isSuperUser">
                    &nbsp;<label class="custom-control-label" for="userIsSuperUser">Is Super User</label>
                </div>
            </div>
        </template>
        <div v-if="formData.id" class="mb-3">
            <div class="custom-control custom-checkbox">
                <input type="checkbox" class="custom-control-input" id="userIsActive" v-model="formData.isActive">
                &nbsp;<label class="custom-control-label" for="userIsActive">Is Active</label>
            </div>
        </div>
    </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal";
import InputEmail from "../inputs/InputEmail";
import InputSelectize from "../inputs/InputSelectize";

export default {
    name: "EditUserModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal, InputEmail, InputSelectize},
    data() {
        return {
            modalName: 'editUserModal',
            crudUrl: 'account-user/',
            isUpdateData: true,
            initDataKey: 'users',
            requiredFields: {
                firstName: '#userFName',
                lastName: '#userLName',
                email: '#userEmail',
                userTypes: null  // Set on mount
            }
        }
    },
    computed: {
        userTypesCfg() {
            return {
                plugins: ['remove_button'],
                maxItems: null,
                options: Object.entries(this.globalData.USER_TYPES).map(([key, txt]) => ({value: key, text: txt}))
            }
        }
    },
    methods: {
        getAjaxCfgOverride() {
            return {method: (this.formData.id) ? 'PUT' : 'POST'};
        },
        processRawData(rawData) {
            const userTypes = Object.keys(this.globalData.USER_TYPES)
                .filter((t) => parseInt(t) & rawData.formData.userTypeBits);
            this.$refs['userTypes'].elSel.setValue(userTypes);
            return Object.assign(rawData.formData, {userTypes});
        },
        processFormData() {
            const formData = this.readForm();
            return Object.assign({}, formData, {userTypeBits: _.sum(formData.userTypes)});
        }
    },
    mounted() {
        this.requiredFields.userTypes = this.$refs['userTypes'].targetEl;
    }
}
</script>
