<template>
    <BaseModal
        :modalId="modalName"
        :modalTitle="(formData.id) ? `Edit employer: ${formData.companyName} (${formData.id})`: 'Create new employer'"
        :primaryButtonText="(formData.id) ? 'Save changes' : 'Create employer'"
        :isAllowDelete="Boolean(formData.id)"
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
                :mediaTypes="['image']"
                itemLabel="company logo"
                :currentItem="formData.logo"
                @selected="formData.logo = $event"
            />
        </div>
    </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal";
import InputOrViewMedia from "../inputs/InputOrViewMedia";

export default {
    name: "EditEmployerModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal, InputOrViewMedia},
    data() {
        return {
            modalName: 'editEmployerModal',
            crudUrl: 'account-employer/',
            isUpdateData: true,
            initDataKey: 'employers',
            requiredFields: {
                companyName: '#employerCompanyName',
            },
            mediaFields: ['logo'],
            isLogoUpload: true
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
    },
    updated() {
        this.toggleLogoUpload(!Boolean(this.formData.logo));
    }
}
</script>