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
        <div class="mb-3">
            <label for="userEmployer" class="form-label">Employer</label>
            <InputSelectize
                ref="userEmployer"
                elId="userEmployer"
                :isParseAsInt="true"
                placeholder="Optional" :cfg="userEmployerCfg" @selected="formData.employerId = $event"
            />
        </div>
        <div class="form-check">
            <InputCheckBox
                v-if="isSuperUser"
                elId="userIsStaff"
                label="Is Staff"
                :isChecked="formData.isStaff"
                :isActiveLabel="true"
                @click="formData.isStaff = $event"
            />
            <InputCheckBox
                v-if="isSuperUser"
                elId="userIsSuperUser"
                label="Is Super User"
                :isChecked="formData.isSuperUser"
                :isActiveLabel="true"
                @click="formData.isSuperUser = $event"
            />
            <InputCheckBox
                elId="userIsActive"
                label="Is Active"
                :isChecked="formData.isActive"
                :isActiveLabel="true"
                @click="formData.isActive = $event"
            />
        </div>
    </BaseModal>
</template>

<script>
import {USER_BITS} from '../../globalData';
import BaseModal from "./BaseModal";
import InputCheckBox from "../inputs/InputCheckBox";
import InputEmail from "../inputs/InputEmail";
import InputSelectize from "../inputs/InputSelectize";
import {severity} from "../../vueMixins";
import dataUtil from "../../utils/data";

export default {
    name: "EditUserModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal, InputCheckBox, InputEmail, InputSelectize},
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
        userEmployerCfg() {
            return {
                maxItems: 1,
                options: this.initData.employers.map((e) => ({value: e.id, text: e.companyName}))
            }
        },
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
                .reduce((userTypes, t) => {
                    const val = parseInt(t);
                    if (val & rawData.formData.userTypeBits) {
                        userTypes.push(val);
                    }
                    return userTypes;
                }, []);
            this.$refs['userTypes'].elSel.setValue(userTypes);
            this.$refs['userEmployer'].elSel.setValue(rawData.formData.employerId);
            return Object.assign(rawData.formData, {userTypes});
        },
        processFormData() {
            const formData = this.readForm();
            return Object.assign({}, formData, {userTypeBits: dataUtil.sum(formData.userTypes)});
        },
        isGoodFormFields(formData) {
            if (formData.userTypes.includes(USER_BITS.EMPLOYER) !== Boolean(formData.employerId)) {
                console.log($(this.$refs.userEmployer.targetEl));
                this.addPopover($(this.$refs.userEmployer.targetEl), {
                    severity: severity.WARN,
                    content: 'Employer and user type of "employer" must both be set',
                    isOnce: true
                });
                return false;
            }
            return true;
        }
    },
    mounted() {
        this.requiredFields.userTypes = this.$refs['userTypes'].targetEl;
    }
}
</script>
