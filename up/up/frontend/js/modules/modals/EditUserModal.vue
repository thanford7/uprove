<template>
    <BaseModal
        :isContentOnly="isContentOnly"
        :modalId="modalName"
        :modalTitle="getModalTitle()"
        :primaryButtonText="(!isAdmin) ? 'Sign up' : (formData.id) ? 'Save changes' : 'Create user'"
        :isAllowDelete="Boolean(formData.id)"
        @saveChange="saveChange($event)"
        @deleteObject="deleteObject($event)"
    >
        <div class="mb-3">
            <label for="userFName" class="form-label">First name</label>
            <input type="text" class="form-control" placeholder="Required" id="userFName" v-model="formData.firstName">
        </div>
        <div class="mb-3">
            <label for="userFName" class="form-label">Last name</label>
            <input type="text" class="form-control" placeholder="Required" id="userLName" v-model="formData.lastName">
        </div>
        <div class="mb-3">
            <label for="userEmail" class="form-label">Email</label>
            <InputEmail elId="userEmail" placeholder="Required" v-model="formData.email"/>
        </div>
        <template v-if="isAdmin && isShowAdminFields" >
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
                    :isChecked="formData.isActive || !formData.id"
                    :isActiveLabel="true"
                    @click="formData.isActive = $event"
                />
                <InputCheckBox
                    elId="userIsDemo"
                    label="Is Demo"
                    :isChecked="formData.isDemo"
                    :isActiveLabel="true"
                    @click="formData.isDemo = $event"
                />
            </div>
        </template>
    </BaseModal>
</template>

<script>
import {SEVERITY, USER_BITS} from '../../globalData';
import BaseModal from "./BaseModal";
import dataUtil from "../../utils/data";
import InfoToolTip from "../components/InfoToolTip";
import InputCheckBox from "../inputs/InputCheckBox";
import InputEmail from "../inputs/InputEmail";
import InputSelectize from "../inputs/InputSelectize";

export default {
    name: "EditUserModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    props: ['isContentOnly', 'isShowAdminFields'],
    components: {BaseModal, InfoToolTip, InputCheckBox, InputEmail, InputSelectize},
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
            },
            successAlertType: SEVERITY.INFO,
            infoBirthDate: 'We don\'t share age or birth date with employers, but we would like to wish you a happy birthday!'
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
        getModalTitle() {
            if (!this.isAdmin) {
                return 'Sign Up';
            }
            if (this.formData.id) {
                return `Edit user: ${this.formData.firstName} ${this.formData.lastName} (${this.formData.id})`;
            }
            return 'Create new user';
        },
        processRawData(rawData) {
            let userTypes;
            if (this.isShowAdminFields) {
                userTypes = Object.keys(this.globalData.USER_TYPES)
                    .reduce((userTypes, t) => {
                        const val = parseInt(t);
                        if (val & rawData.userTypeBits) {
                            userTypes.push(val);
                        }
                        return userTypes;
                    }, []);
                this.$refs.userTypes.elSel.setValue(userTypes);
                this.$refs.userEmployer.elSel.setValue(rawData.employerId);
            }
            return Object.assign(rawData, {userTypes});
        },
        processFormData() {
            const formData = this.readForm();
            let {next, inviteEmployerId} = dataUtil.getQueryParams();
            if (next) {
                formData.next = next;
            }

            inviteEmployerId = parseInt(inviteEmployerId);
            if (inviteEmployerId) {
                formData.inviteEmployerId = inviteEmployerId;
            }

            return Object.assign(
                formData,
                {userTypeBits: dataUtil.sum(formData.userTypes)}
            );
        },
        isGoodFormFields(formData) {
            if (this.$refs.userTypes && formData.userTypes.includes(USER_BITS.EMPLOYER) !== Boolean(formData.employerId)) {
                this.addPopover($(this.$refs.userEmployer.targetEl), {
                    severity: SEVERITY.WARN,
                    content: 'Employer and user type of "employer" must both be set',
                    isOnce: true
                });
                return false;
            }
            return true;
        },
        getSuccessMessage(data, method) {
            const userName = `${data.firstName} ${data.lastName}`;
            if (method === 'POST') {
                return (
                    `Account created for ${userName}. Email sent to ${data.email} to set your ` +
                    `password. If you didn\'t receive it, use the "reset password" link or email community@uprove.co`
                )
            }
            if (method === 'PUT') {
                return `Updated ${userName}'s account`;
            }
            return 'Deleted account';
        },
    },
    mounted() {
        if (this.$refs.userTypes) {
            this.requiredFields.userTypes = this.$refs.userTypes.targetEl;
        }
    }
}
</script>
