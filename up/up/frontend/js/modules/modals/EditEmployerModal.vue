<template>
    <BaseModal
        :modalId="modalName"
        :modalTitle="(formData.id) ? `Edit employer: ${formData.companyName} (${formData.id})`: 'Create new employer'"
        :primaryButtonText="(formData.id) ? 'Save changes' : 'Create employer'"
        :isAllowDelete="Boolean(formData.id)"
        :isLargeDisplay="true"
        @saveChange="saveChange($event)"
        @deleteObject="deleteObject($event)"
    >
        <div class="mb-3">
            <label for="employerCompanyName" class="form-label">Company name</label>
            <input type="text" class="form-control" placeholder="Required" id="employerCompanyName" v-model="formData.companyName">
        </div>
        <div class="mb-3">
            <InputOrViewMedia
                inputId="employerLogo"
                :mediaTypes="[contentTypes.IMAGE]"
                itemLabel="company logo"
                :currentItem="formData.logo"
                @selectedMediaNew="formData.logo = $event"
            />
        </div>
        <div class="mb-3">
            <label for="employerDescription" class="form-label">Company description</label>
            <InputWsiwyg v-model="formData.description" elId="employerDescription" placeholder="Add description..."/>
        </div>
        <div class="mb-3">
            <label for="companySize" class="form-label">Company size</label>
            <InputSelectize
                ref="companySize"
                :elId="getNewElUid()"
                :cfg="{
                    valueField: 'id',
                    labelField: 'companySize',
                    maxItems: 1,
                    options: initData.companySizes,
                }"
                :isParseAsInt="true"
                :items="formData.companySizeId"
                placeholder="Optional"
                @selected="formData.companySizeId = $event"
            />
        </div>
        <div class="mb-3">
            <label for="glassdoorUrl" class="form-label">Glassdoor URL</label>
            <input type="text" class="form-control" placeholder="Optional" id="glassdoorUrl" v-model="formData.glassDoorUrl">
        </div>
        <div v-if="isAdmin" class="form-check">
            <InputCheckBox
                elId="employerIsDemo"
                label="Is Demo"
                :isChecked="formData.isDemo"
                :isActiveLabel="true"
                @click="formData.isDemo = $event"
            />
            <InputCheckBox
                elId="employerIsClient"
                label="Is Client"
                :isChecked="formData.isClient"
                :isActiveLabel="true"
                @click="formData.isClient = $event"
            />
        </div>
    </BaseModal>
</template>

<script>
import {CONTENT_TYPES} from '../../globalData';
import BaseModal from "./BaseModal";
import InputCheckBox from "../inputs/InputCheckBox";
import InputOrViewMedia from "../inputs/InputOrViewMedia";
import InputSelectize from "../inputs/InputSelectize";
import InputWsiwyg from "../inputs/InputWsiwyg";
import dataUtil from "../../utils/data";

export default {
    name: "EditEmployerModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    props: ['isUpdateDataOverride'],
    components: {BaseModal, InputCheckBox, InputOrViewMedia, InputSelectize, InputWsiwyg},
    data() {
        return {
            modalName: 'editEmployerModal',
            crudUrl: 'account-employer/',
            isHardRefresh: true,
            requiredFields: {
                companyName: '#employerCompanyName',
            },
            mediaFields: new Set(['logo']),
            isLogoUpload: true,
            contentTypes: CONTENT_TYPES
        }
    },
    methods: {
        processRawData(rawData) {
            return rawData;
        },
        toggleLogoUpload(isShown) {
            this.isLogoUpload = isShown;
            $('#employerLogo').toggle(isShown);
        }
    },
    mounted() {
        this.toggleLogoUpload(!Boolean(this.formData.logo));
        if (!dataUtil.isNil(this.isUpdateDataOverride)) {
            this.isUpdateData = this.isUpdateDataOverride;
        }
    },
    updated() {
        this.toggleLogoUpload(!Boolean(this.formData.logo));
    }
}
</script>