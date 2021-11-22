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
            <label for="employerLogo" class="form-label">Company logo</label>
            <div v-if="formData.logo && !isLogoUpload" class="mb-1">
                <img :src="formData.logo" style="height: 40px;"><br>
                <a href="#" @click="toggleLogoUpload(true)">Change logo</a>
            </div>
            <InputMedia elId="employerLogo" :mediaTypes="['image']" @selected="formData.logo = $event"/>
            <a v-if="formData.logo && isLogoUpload" href="#" @click="toggleLogoUpload(false)">Use existing logo</a>
        </div>
    </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal";
import InputMedia from "../inputs/InputMedia";

export default {
    name: "EditEmployerModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal, InputMedia},
    data() {
        return {
            modalName: 'editEmployerModal',
            crudUrl: 'account-employer/',
            requiredFields: {
                companyName: 'employerCompanyName',
            },
            fileFields: ['logo'],
            isLogoUpload: true
        }
    },
    methods: {
        processRawData(rawData) {
            console.log(rawData);
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