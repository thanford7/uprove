<template>
    <BaseModal
        :modalId="modalName"
        modalTitle="Edit education"
        :isContentOnly="isContentOnly"
        :isScrollable="true"
        :isLargeDisplay="true"
        @saveChange="saveChange"
    >
        <div class="mb-3">
            <label class="form-label">School name</label>
            <InputSelectize
                ref="schoolName"
                :elId="getNewElUid()"
                :cfg="orgCfg"
                @selected="setSchoolData"
                placeholder="Start typing to find existing schools or create a new one"
            />
        </div>
        <div v-if="formData?.school?.name" class="mb-3">
            <InputOrViewMedia
                :inputId="getNewElUid()"
                :mediaTypes="[contentTypes.IMAGE]"
                :itemLabel="`${formData.school.name} logo`"
                :currentItem="formData.school.logo"
                :isUploadDefault="!formData.school.logo"
                @selectedMediaNew="formData.school.newLogo = $event"
            />
        </div>
        <div class="row mb-3">
            <div class="col-md-3">
                <label class="form-label">Start date</label>
                <InputMonthYear :value="formData.startDate" @change="formData.startDate = $event"/>
            </div>
            <div class="col-md-3">
                <label class="form-label">End date</label>
                <InputMonthYear :value="formData.endDate" @change="formData.endDate = $event"/>
            </div>
        </div>
        <div class="mb-3">
            <label class="form-label">Degree type</label>
            <InputSelectize
                :elId="getNewElUid()"
                :cfg="degreeCfg"
                :items="formData.degree"
                placeholder="Select degree type"
                @selected="this.formData.degree = $event"
            />
        </div>
        <div class="mb-3">
            <label class="form-label">Degree subject</label>
            <input type="text" class="form-control" placeholder="Add degree subject..." v-model="formData.degreeSubject">
        </div>
        <div class="mb-3">
            <label class="form-label">Activities</label>
            <InputWsiwyg placeholder="Add activities..." v-model="formData.activities"/>
        </div>
    </BaseModal>
</template>
<script>
import {CONTENT_TYPES, DEGREE_OPTIONS, ORGANIZATION_TYPES} from '../../globalData';
import BaseModal from './BaseModal.vue';
import InputMonthYear from '../inputs/InputMonthYear.vue';
import InputOrViewMedia from "../inputs/InputOrViewMedia";
import InputSelectize from "../inputs/InputSelectize";
import InputSelectOrUploadMedia from "../inputs/InputSelectOrUploadMedia";
import InputWsiwyg from '../inputs/InputWsiwyg.vue';
import orgSelectize from "../selectizeCfgs/organization";

export default {
    extends: BaseModal,
    inheritAttrs: false,
    props: ['isContentOnly'],
    data() {
        return {
            modalName: 'editEducationModal',
            crudUrl: 'user-profile/content-item/',
            isUpdateData: true,
            formData: this.getEmptyFormData(),
            requiredFields: {
                'school.name': null
            },
            mediaFields: ['school.newLogo'],
            contentTypes: CONTENT_TYPES,
            orgCfg: orgSelectize.getOrgCfg(ORGANIZATION_TYPES.SCHOOL),
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
    components: {BaseModal, InputMonthYear, InputOrViewMedia, InputSelectize, InputSelectOrUploadMedia, InputWsiwyg},
    methods: {
        getEmptyFormData() {
            return {school: {}}
        },
        processFormData() {
            return Object.assign(this.readForm(), {
                userId: this.initData.user.id,
                type: this.contentTypes.EDUCATION,
                profileId: (this.initData.sections) ? this.initData.id : null
            });
        },
        setFormFields() {
            const schoolSel = this.$refs.schoolName.elSel;
            schoolSel.addOption(this.formData.school);
            schoolSel.refreshOptions();
            schoolSel.addItem(this.formData.school.id, true);
        },
        setSchoolData(val) {
            const id = parseInt(val);
            if (id) {
                this.formData.schoolId = id;
                Object.assign(this.formData, this.getEmptyFormData()); // Clear school data
            } else {
                this.formData.school.name = val;
                this.formData.school.orgType = ORGANIZATION_TYPES.SCHOOL
                this.formData.schoolId = null;
            }
        }
    },
    mounted() {
        this.requiredFields['school.name'] = this.$refs.schoolName.targetEl;
    },
}
</script>