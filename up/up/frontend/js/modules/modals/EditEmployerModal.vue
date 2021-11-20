<template>
    <BaseModal
        :modalId="modalName"
        @saveChange="saveChange($event)"
    >
        <div class="mb-3">
            <label for="employerCompanyName" class="form-label">Company name</label>
            <input type="text" class="form-control" placeholder="Required" id="employerCompanyName" v-model="formData.companyName">
        </div>
        <div class="mb-3">
            <label for="employerLogo" class="form-label">Company logo</label>
            <input type="text" class="form-control" placeholder="Optional" id="employerLogo" v-model="formData.logo">
        </div>
    </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal";

export default {
    name: "EditEmployerModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal},
    data() {
        return {
            modalName: 'editEmployerModal',
            crudUrl: 'account-employer/',
            requiredFields: {
                companyName: 'employerCompanyName',
            }
        }
    },
    methods: {
        getAjaxCfgOverride() {
            return {method: 'POST'};
        }
    }
}
</script>