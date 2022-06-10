<template>
    <BaseModal
        :modalId="modalName"
        modalTitle="Edit job preferences"
        primaryButtonText="Save changes"
        @saveChange="savePreferences"
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
        <div class="mb-3">
            <label class="form-label">
                Minimum acceptable salary
                <InfoToolTip :elId="getNewElUid()" content="We will never show this to employers. We use it to filter out jobs that won't be of interest to you."/>
            </label>
            <RangeSlider
                ref="salary"
                :elId="getNewElUid()"
                :min="30000" :max="250000" title="Salary"
                :isPct="false" :step="5000" :valueFormatFn="formatCurrency"
                @changed="formData.salary = $event"
            />
        </div>
    </BaseModal>
</template>

<script>
import {REMOTE_BITS} from '../../globalData';
import BaseModal from "./BaseModal";
import InfoToolTip from "../components/InfoToolTip";
import InputSelectize from "../inputs/InputSelectize";
import RangeSlider from "../components/RangeSlider";
import dataUtil from "../../utils/data";

export default {
    name: "EditJobPreferencesModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal, InfoToolTip, InputSelectize, RangeSlider},
    props: ['isResetUrl'],
    data() {
        return {
            modalName: 'editJobPreferencesModal',
            crudUrl: 'user-preferences/',
            loadRoutes: [{route: 'preferences/', dataKey: 'preferences'}],
            isHardRefresh: true,
        }
    },
    methods: {
        formatCurrency: dataUtil.formatCurrency,
        getAjaxCfgOverride() {
            return {method: 'PUT'};
        },
        getSplitRemoteBits(remoteBits) {
            return Object.values(REMOTE_BITS).filter((bit) => parseInt(bit) & remoteBits);
        },
        setFormFields() {
            this.$refs.companySize.elSel.setValue(this.formData?.companySizes?.map((c) => c.id));
            this.$refs.country.elSel.setValue(this.formData?.countries?.map((c) => c.id));
            this.$refs.remote.elSel.setValue(this.getSplitRemoteBits(this.formData.remoteBits));
            this.$refs.salary.setValue(this.formData?.salary)
        },
        savePreferences(val) {
            this.saveChange(val)
            if (this.isResetUrl) {
                this.isHardRefresh = false;
                this.pageRedirect = dataUtil.getUrlWithoutQueryParams();
            }
        }
    },
    async created() {
        await this.loadData();
        this.$refs.companySize.resetOptions(this.cData.preferences.companySizes);
        this.$refs.country.resetOptions(this.cData.preferences.countries);
    }
}
</script>