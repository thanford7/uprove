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
            <label for="userLName" class="form-label">Last name</label>
            <input type="text" class="form-control" placeholder="Required" id="userLName" v-model="formData.lastName">
        </div>
        <div class="mb-3">
            <label for="userEmail" class="form-label">Email</label>
            <InputEmail elId="userEmail" placeholder="Required" v-model="formData.email"/>
        </div>
        <div v-if="isAdmin && isShowAdminFields" class="mb-3">
            <label for="userPassword" class="form-label">
                Password
                <InfoToolTip :elId="getNewElUid()" :isHtmlContent="true" :content="passwordRequirementInfo"/>
            </label>
            <input type="password" class="form-control" id="userPassword" placeholder="Optional (auto-generated)" v-model="formData.password">
        </div>
        <LocationInputs ref="locationInputs" :formData="formData"/>
        <template v-if="isAdmin && isShowAdminFields">
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
import employersSelectize from "../selectizeCfgs/employers";
import InfoToolTip from "../components/InfoToolTip";
import InputCheckBox from "../inputs/InputCheckBox";
import InputEmail from "../inputs/InputEmail";
import InputSelectize from "../inputs/InputSelectize";
import LocationInputs from "../inputs/LocationInputs";

export default {
    name: "EditUserModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    props: ['isContentOnly', 'isShowAdminFields', 'isUpdateDataOverride', 'isHardRefreshOverride'],
    components: {BaseModal, InfoToolTip, InputCheckBox, InputEmail, InputSelectize, LocationInputs},
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
            passwordRequirementInfo: `
                <div>
                    Password must have:
                    <ul>
                        <li>8 characters minimum</li>
                        <li>At least 1 lowercase letter</li>
                        <li>At least 1 uppercase letter</li>
                        <li>At least 1 number</li>
                        <li>At least one symbol</li>
                    </ul>
                </div>
            `
        }
    },
    computed: {
        userEmployerCfg() {
            return employersSelectize.getEmployersCfg();
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
                this.$refs.userEmployer.elSel.load(
                    employersSelectize.loadEmployerByIdFn(rawData.employerId, this.$refs.userEmployer)
                );
            }
            this.$refs.locationInputs.setStateVal(rawData.stateId);
            this.$refs.locationInputs.setCountryVal(rawData.countryId);
            return Object.assign(rawData, {userTypes});
        },
        processFormData() {
            const formData = this.readForm();
            let {next, inviteEmployerId, waitlistType} = dataUtil.getQueryParams();
            if (next) {
                formData.next = next;
            }
            if (waitlistType) {
                formData.waitlistType = waitlistType;
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
        isGoodPassword(password) {
            return (
                password.length >= 8
                && password.search(/[A-Z]/) >= 0
                && password.search(/[a-z]/) >= 0
                && password.search(/[0-9]/) >= 0
                && password.search(/[^A-Za-z0-9]/) >=0
                && password.search(/\s/) === -1
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

            if (formData.password && !this.isGoodPassword(formData.password)) {
                this.addPopover($('#userPassword'), {
                    severity: SEVERITY.WARN,
                    content: 'Password does not meet requirements',
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
    async mounted() {
        this.isHardRefresh = this.isHardRefreshOverride;
        if (this.$refs.userTypes) {
            this.requiredFields.userTypes = this.$refs.userTypes.targetEl;
        }
        if (!dataUtil.isNil(this.isUpdateDataOverride)) {
            this.isUpdateData = this.isUpdateDataOverride;
        }
    },
}
</script>
