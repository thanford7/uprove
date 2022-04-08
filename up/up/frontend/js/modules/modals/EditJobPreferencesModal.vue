<template>
    <BaseModal
        :modalId="modalName"
        modalTitle="Edit job preferences"
        primaryButtonText="Save changes"
        @saveChange="saveChange($event)"
    >
        <div class="mb-3">
            <label class="form-label">Company size</label>
            <InputSelectize
                ref="companySize"
                :elId="getNewElUid()"
                :cfg="{
                    valueField: 'id',
                    labelField: 'companySize',
                    maxItems: null,
                    plugins: ['remove_button'],
                }"
                :isParseAsInt="true"
                placeholder="Optional"
                @selected="formData.companySizes = $event"
            />
        </div>
        <div class="mb-3">
            <label class="form-label">Roles</label>
            <InputSelectize
                ref="role"
                :elId="getNewElUid()"
                :cfg="{
                    valueField: 'id',
                    labelField: 'roleTitle',
                    maxItems: null,
                    plugins: ['remove_button'],
                }"
                :isParseAsInt="true"
                placeholder="Optional"
                @selected="formData.roleTitles = $event"
            />
        </div>
        <div class="mb-3">
            <label class="form-label">Countries</label>
            <InputSelectize
                ref="country"
                :elId="getNewElUid()"
                :cfg="{
                    valueField: 'id',
                    labelField: 'countryName',
                    maxItems: null,
                    plugins: ['remove_button'],
                }"
                :isParseAsInt="true"
                placeholder="Optional"
                @selected="formData.countries = $event"
            />
        </div>
        <div class="mb-3">
            <label class="form-label">Remote preference</label>
            <InputSelectize
                ref="remote"
                :elId="getNewElUid()"
                :cfg="{
                    valueField: 'val',
                    labelField: 'title',
                    maxItems: null,
                    plugins: ['remove_button'],
                    options: [
                        {val: 1, title: 'Non-remote'},
                        {val: 2, title: 'Remote'}
                    ],
                }"
                :isParseAsBits="true"
                placeholder="Optional"
                @selected="formData.remote = $event"
            />
        </div>
    </BaseModal>
</template>

<script>
import {REMOTE_BITS} from '../../globalData';
import BaseModal from "./BaseModal";
import InputSelectize from "../inputs/InputSelectize";

export default {
    name: "EditJobPreferencesModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal, InputSelectize},
    data() {
        return {
            modalName: 'editJobPreferencesModal',
            crudUrl: 'user-preferences/',
            loadRoutes: [{route: 'preferences/', dataKey: 'preferences'}],
            isHardRefresh: true,
        }
    },
    methods: {
        getAjaxCfgOverride() {
            return {method: 'PUT'};
        },
        getSplitRemoteBits(remoteBits) {
            return Object.values(REMOTE_BITS).filter((bit) => parseInt(bit) & remoteBits);
        },
        setFormFields() {
            this.$refs.companySize.elSel.setValue(this.formData?.companySizes?.map((c) => c.id));
            this.$refs.role.elSel.setValue(this.formData?.roles?.map((r) => r.id));
            this.$refs.country.elSel.setValue(this.formData?.countries?.map((c) => c.id));
            this.$refs.remote.elSel.setValue(this.getSplitRemoteBits(this.formData.remoteBits));
        }
    },
    async created() {
        await this.loadData();
        this.$refs.companySize.resetOptions(this.cData.preferences.companySizes);
        this.$refs.role.resetOptions(this.cData.preferences.roleTitles);
        this.$refs.country.resetOptions(this.cData.preferences.countries);
    }
}
</script>