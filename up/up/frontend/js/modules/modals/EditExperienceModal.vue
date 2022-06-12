<template>
    <BaseModal
        :modalId="modalName"
        modalTitle="Edit experience"
        :isLargeDisplay="true"
        :isContentOnly="isContentOnly"
        @saveChange="saveChange"
    >
        <div class="mb-3">
            <label class="form-label">Company or organization</label>
            <InputSelectize
                ref="orgName"
                :elId="getNewElUid()"
                :cfg="orgCfg"
                @selected="setOrganizationData"
                placeholder="Start typing to find existing organizations or create a new one"
            />
        </div>
        <div v-if="formData.organization && formData.organization.name" class="mb-3">
            <InputOrViewMedia
                :inputId="getNewElUid()"
                :mediaTypes="[contentTypes.IMAGE]"
                :itemLabel="`${formData.organization.name} logo`"
                :currentItem="formData.organization.logo"
                :isUploadDefault="!formData.organization.logo"
                @selectedMediaNew="formData.organization.newLogo = $event"
            />
        </div>
        <div class="mb-3">
            <label for="positionTitle" class="form-label">Position title</label>
            <input id="positionTitle" type="text" class="form-control" placeholder="Add title..." v-model="formData.positionTitle">
        </div>
        <div class="mb-3">
            <label class="form-label">Employment type</label>
            <InputSelectize
                ref="employmentType"
                :elId="getNewElUid()"
                :items="formData.employmentType"
                :cfg="employmentTypeSelCfg"
                @selected="formData.employmentType = $event"
                placeholder="Select type..."
            />
        </div>
        <div class="row mb-3">
            <div id="startDate" class="col-lg-3 col-md-4">
                <label class="form-label">Start month</label>
                <InputMonthYear ref="startDate"  :value="formData.startDate" @change="formData.startDate = $event"/>
            </div>
            <div class="col-lg-3 col-md-4">
                <label class="form-label">End month</label>
                <InputMonthYear ref="endDate" :value="formData.endDate" @change="formData.endDate = $event"/>
            </div>
        </div>
        <div class="mb-3">
            <label class="form-label" for="employmentDescription">Description</label>
            <InputWsiwyg
                placeholder="Add description of position..."
                v-model="formData.description"
            />
        </div>
    </BaseModal>
</template>
<script>
import {CONTENT_TYPES, SEVERITY, ORGANIZATION_TYPES} from '../../globalData';
import BaseModal from './BaseModal.vue';
import InputOrViewMedia from "../inputs/InputOrViewMedia";
import InputMonthYear from '../inputs/InputMonthYear.vue';
import InputSelectize from '../inputs/InputSelectize.vue';
import InputSelectOrUploadMedia from '../inputs/InputSelectOrUploadMedia.vue';
import InputWsiwyg from '../inputs/InputWsiwyg.vue';
import mediaSelectize from "../selectizeCfgs/media";
import orgSelectize from "../selectizeCfgs/organization";
import dataUtil from "../../utils/data";

export default {
    extends: BaseModal,
    props: ['isContentOnly'],
    data() {
        return {
            modalName: 'editExperienceModal',
            crudUrl: 'user-profile/content-item/',
            isUpdateData: true,
            formData: this.getDefaultForm(),
            requiredFields: {
                positionTitle: '#positionTitle',
                startDate: '#startDate',
                employmentType: null
            },
            mediaFields: new Set(['organization.newLogo']),
            employmentTypeSelCfg: {
                options: [
                    {name: 'Full-time'},
                    {name: 'Part-time'},
                    {name: 'Self-employed'},
                    {name: 'Contracted'},
                    {name: 'Internship'}
                ],
                maxItems: 1,
                valueField: 'name',
                labelField: 'name'
            },
            orgCfg: orgSelectize.getOrgCfg({orgType: ORGANIZATION_TYPES.COMPANY}),
            contentTypes: CONTENT_TYPES,
            mediaSelectize
        }
    },
    watch: {
        formData(newVal) {
            if (!newVal) {
                this.formData = this.getDefaultForm();
            } else if (!newVal.organization) {
                Object.assign(newVal, this.getDefaultForm());
            }
        }
    },
    inheritAttrs: false,
    components: {BaseModal, InputMonthYear, InputOrViewMedia, InputSelectize, InputSelectOrUploadMedia, InputWsiwyg},
    methods: {
        getDefaultForm() {
            return {organization: {orgType: ORGANIZATION_TYPES.COMPANY}};
        },
        isGoodFormFields(formData) {
            if (!formData.organizationId) {
                if (!formData.organization.name) {
                    this.addPopover($(`#${this.$refs.orgName.targetEl}`),
                        {severity: SEVERITY.WARN, content: 'Organization name is required', isOnce: true}
                    );
                    return false;
                }
            }
            if (formData.startDate && formData.endDate && !dataUtil.convertToDayJS(formData.endDate).isAfter(formData.startDate)) {
                this.addPopover($(`#${this.$refs.endDate.elId}`),
                    {severity: SEVERITY.WARN, content: 'End month must be after start month', isOnce: true}
                );
                return false;
            }
            return true
        },
        processFormData() {
            return Object.assign(this.readForm(), {
                userId: this.initData.user.id,
                type: CONTENT_TYPES.EXPERIENCE,
                profileId: (this.initData.sections) ? this.initData.id : null
            });
        },
        processRawData(rawData) {
            this.requiredFields.employmentType = `#${this.$refs.employmentType.targetEl}`;
            this.requiredFields.startDate = `#${this.$refs.startDate.elId}`;
            return Object.assign(
                this.getDefaultForm(),
                rawData || {}
            );
        },
        setFormFields() {
            const orgSel = this.$refs.orgName.elSel;
            orgSel.addOption(this.formData.organization);
            orgSel.refreshOptions();
            orgSel.addItem(this.formData.organization.id, true);
        },
        setOrganizationData(val) {
            const id = parseInt(val);
            if (id) {
                this.formData.organizationId = id;
                Object.assign(this.formData, this.getDefaultForm()); // Clear organization data
            } else {
                this.formData.organization.name = val;
                this.formData.organizationId = null;
            }
        }
    },
    mounted() {
        this.requiredFields.employmentType = this.$refs.employmentType.targetEl;
    }
}
</script>