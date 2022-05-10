<template>
    <BaseModal
        :modalId="modalName"
        :modalTitle="(formData.id) ? `Edit posting: ${formData.jobTitle}`: 'Create new posting'"
        :primaryButtonText="(formData.id) ? 'Save changes' : 'Create posting'"
        :isLargeDisplay="true"
        :isScrollable="true"
        :isAllowDelete="Boolean(formData.id)"
        @saveChange="saveChange($event)"
        @deleteObject="deleteObject($event)"
    >
        <div class="mb-3">
            <label for="modalJobTitle" class="form-label">Job Title</label>
            <input type="text" class="form-control" placeholder="Required" id="modalJobTitle" v-model="formData.jobTitle">
        </div>
        <div class="mb-3">
            <label class="form-label">Standardized Role</label>
            <InputSelectize
                ref="role"
                :elId="getNewElUid()"
                :items="formData.roleLevelId"
                :cfg="{
                    valueField: 'id',
                    labelField: 'roleTitle',
                    searchField: 'roleTitle',
                    maxItems: 1,
                    options: initData.roleLevels
                }"
                :isParseAsInt="true"
                placeholder="Optional"
                @selected="formData.roleLevelId = $event"
            />
        </div>
        <LocationInputs ref="locationInputs" :formData="formData"/>
        <div class="mb-3">
            <label for="modalJobDescription" class="form-label">Job Description</label>
            <InputWsiwyg
                ref="jobDescription"
                elId="modalJobDescription"
                placeholder="Add a description..."
                v-model="formData.jobDescription"
            />
            <div class="row align-items-center">
                <div class="col-5 pe-0">
                    <InputSelectize
                        ref="jobTemplate"
                        elId="modalJobTemplate"
                        :isParseAsInt="true"
                        placeholder="Start from template" :cfg="templateCfg" @selected="updateJobDescription"
                    />
                </div>
                <div class="col-1 ps-1">
                    <InfoToolTip :elId="getNewElUid()" :content="infoJobTemplate"/>
                </div>
            </div>
        </div>
        <div class="mb-3">
            <label for="openDate" class="form-label">Open Date <InfoToolTip :content="TOOLTIPS.jobStartDate" :elId="getNewElUid()"/></label>
            <input type="date" class="form-control" id="openDate" v-model="formData.openDate">
            <span class="-sub-text">Leave blank for "DRAFT" status</span>
        </div>
        <div v-if="formData.id" class="mb-3">
            <label for="pauseDate" class="form-label">Pause Date <InfoToolTip :content="TOOLTIPS.jobPauseDate" :elId="getNewElUid()"/></label>
            <input type="date" class="form-control" id="pauseDate" v-model="formData.pauseDate">
        </div>
        <div v-if="formData.id" class="mb-3">
            <label for="closeDate" class="form-label">Close Date <InfoToolTip :content="TOOLTIPS.jobCloseDate" :elId="getNewElUid()"/></label>
            <input type="date" class="form-control" id="closeDate" v-model="formData.closeDate">
        </div>
    </BaseModal>
</template>

<script>
import {SEVERITY} from '../../globalData';
import BaseModal from "./BaseModal";
import form from "../../utils/form";
import InfoToolTip from "../components/InfoToolTip";
import InputSelectize from "../inputs/InputSelectize";
import InputWsiwyg from "../inputs/InputWsiwyg";
import LocationInputs from "../inputs/LocationInputs";
import $ from "jquery";

export default {
    name: "EditJobPostingModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    components: {
        BaseModal, InfoToolTip, InputSelectize, InputWsiwyg, LocationInputs,
    },
    data() {
        return {
            modalName: 'editJobPostingModal',
            crudUrl: 'job-posting/',
            isUpdateData: true,
            initDataKey: 'employer.jobs',
            requiredFields: {
                jobTitle: '#modalJobTitle',
                jobDescription: '#modalJobDescription',
            },
            infoJobTemplate: (
                'Selecting a job template will add suggested language for a job description to the job description ' +
                'section above. If a description already exists, it will NOT be erased. The suggested language will ' +
                'be added to the end of the text.'
            )
        }
    },
    computed: {
        templateCfg() {
            return {
                maxItems: 1,
                sortField: 'text',
                options: this.initData.jobTemplates.map((e) => ({value: e.id, text: e.title}))
            }
        },
    },
    methods: {
        processFormData() {
            return Object.assign(this.readForm(), {employerId: this.initData.employer.id})
        },
        setFormFields() {
            this.$refs.locationInputs.setStateVal(this.formData.stateId);
            this.$refs.locationInputs.setCountryVal(this.formData.countryId);
        },
        isGoodFormFields(formData) {
            if (form.isEmptyWysiwyg(formData.jobDescription)) {
                this.addPopover($('#modalJobDescription'),
                {severity: SEVERITY.WARN, content: 'Required field', isOnce: true}
                    );
                return false;
            }

            return true;
        },
        updateJobDescription(templateId) {
            if (!templateId) {
                return;
            }
            const template = this.initData.jobTemplates.find((jt) => jt.id === templateId);
            this.$refs.jobDescription.addContent(template.description);
        }
    },

}
</script>