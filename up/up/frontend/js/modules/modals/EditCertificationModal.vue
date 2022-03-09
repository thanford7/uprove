<template>
    <BaseModal
        :modalId="modalName"
        modalTitle="Edit license or certification"
        :isContentOnly="isContentOnly"
        :isScrollable="true"
        :isLargeDisplay="true"
        @saveChange="saveChange"
    >
        <div class="mb-3">
            <label class="form-label">Name</label>
            <input type="text" class="form-control" placeholder="Add license or certificate name..." v-model="formData.title">
        </div>
        <div class="mb-3">
            <label class="form-label">Issuing organization</label>
            <InputSelectize
                ref="orgName"
                :elId="getNewElUid()"
                :cfg="orgCfg"
                @selected="setOrganizationData"
                placeholder="Start typing to find existing organizations or create a new one"
            />
        </div>
        <div v-if="formData?.organization?.name" class="mb-3">
            <InputOrViewMedia
                :inputId="getNewElUid()"
                :mediaTypes="[contentTypes.IMAGE]"
                :itemLabel="`${formData.organization.name} logo`"
                :currentItem="formData.organization.logo"
                :isUploadDefault="!formData.organization.logo"
                @selectedMediaNew="formData.organization.newLogo = $event"
            />
        </div>
        <div class="mb-3 form-check">
            <InputCheckBox
                label="This credential has no expiration"
                :isChecked="!formData.hasExpiration"
                :isActiveLabel="true"
                @click="formData.hasExpiration = !$event"
            />
        </div>
        <div class="row mb-3">
            <div class="col-md-3">
                <label class="form-label">Issue date</label>
                <InputMonthYear :value="formData.issueDate" @change="formData.issueDate = $event"/>
            </div>
            <div v-if="formData.hasExpiration" class="col-md-3">
                <label class="form-label">Expiration date</label>
                <InputMonthYear :value="formData.expirationDate" @change="formData.expirationDate = $event"/>
            </div>
        </div>
    </BaseModal>
</template>
<script>
import {CONTENT_TYPES, DEGREE_OPTIONS, ORGANIZATION_TYPES} from '../../globalData';
import BaseModal from './BaseModal.vue';
import InputCheckBox from "../inputs/InputCheckBox";
import InputMonthYear from '../inputs/InputMonthYear.vue';
import InputOrViewMedia from "../inputs/InputOrViewMedia";
import InputSelectize from "../inputs/InputSelectize";
import InputSelectOrUploadMedia from "../inputs/InputSelectOrUploadMedia";
import orgSelectize from "../selectizeCfgs/organization";

export default {
    extends: BaseModal,
    inheritAttrs: false,
    props: ['isContentOnly'],
    data() {
        return {
            modalName: 'editCertificationModal',
            crudUrl: 'user-profile/content-item/',
            isUpdateData: true,
            formData: this.getEmptyFormData(),
            requiredFields: {
                'organization.name': null
            },
            mediaFields: new Set(['organization.newLogo']),
            contentTypes: CONTENT_TYPES,
            orgCfg: orgSelectize.getOrgCfg({orgType: ORGANIZATION_TYPES.SCHOOL}),
            degreeCfg: {
                options: DEGREE_OPTIONS.map((o) => ({type: o})),
                valueField: 'type',
                labelField: 'type',
                searchField: ['type'],
                maxItems: 1,
                create: true,
                persist: false,
                hideSelected: true
            }
        }
    },
    components: {
        BaseModal, InputCheckBox, InputMonthYear, InputOrViewMedia, InputSelectize,
        InputSelectOrUploadMedia
    },
    methods: {
        getEmptyFormData() {
            return {organization: {}}
        },
        processFormData() {
            const formData = this.readForm();
            if (!formData.hasExpiration) {
                formData.existingContentId = null;
            }
            return Object.assign(this.readForm(), {
                userId: this.initData.user.id,
                type: this.contentTypes.CERTIFICATION,
                profileId: (this.initData.sections) ? this.initData.id : null
            });
        },
        setFormFields() {
            const schoolSel = this.$refs.orgName.elSel;
            schoolSel.addOption(this.formData.organization);
            schoolSel.refreshOptions();
            schoolSel.addItem(this.formData.school.id, true);
        },
        setOrganizationData(val) {
            const id = parseInt(val);
            if (id) {
                this.formData.organizationId = id;
                Object.assign(this.formData, this.getEmptyFormData()); // Clear school data
            } else {
                this.formData.organization.name = val;
                this.formData.organization.orgType = ORGANIZATION_TYPES.SCHOOL
                this.formData.organizationId = null;
            }
        }
    },
    mounted() {
        this.requiredFields['organization.name'] = this.$refs.orgName.targetEl;
    },
}
</script>