<template>
    <BaseModal
        :modalId="modalName"
        modalTitle="Edit experience"
        :isLargeDisplay="true"
        :isContentOnly="isContentOnly"
        @saveChange="saveChange"
    >
        <div class="mb-3">
            <label for="formProfileName" class="form-label">Company or organization</label>
            <input type="text" class="form-control" placeholder="Add name..." v-model="formData.organization.name">
        </div>
        <div class="mb-3">
            <label class="form-label">Logo</label>
            <InputSelectOrUploadMedia
                ref="logoPic"
                :mediaTypes="['image']"
                placeholderDescription="Logo picture"
            />
        </div>
        <div class="mb-3">
            <label for="positionTitle" class="form-label">Position title</label>
            <input type="text" class="form-control" placeholder="Add title..." v-model="formData.positionTitle">
        </div>
        <div class="mb-3">
            <label for="employmentType" class="form-label">Employment type</label>
            <InputSelectize
                :elId="getNewElUid()"
                :currentItem="formData.employmentType"
                :cfg="employmentTypeSelCfg"
                @selected="formData.employmentType = $event"
                placeholder="Select type..."
            />
        </div>
        <div class="row mb-3">
            <div class="col-md-3">
                <label class="form-label" for="employmentStartDate">Start date</label>
                <InputMonthYear v-model="formData.startDate"/>
            </div>
            <div class="col-md-3">
                <label class="form-label" for="employmentEndDate">End date</label>
                <InputMonthYear v-model="formData.endDate"/>
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
import BaseModal from './BaseModal.vue';
import InputMonthYear from '../inputs/InputMonthYear.vue';
import InputSelectize from '../inputs/InputSelectize.vue';
import InputSelectOrUploadMedia from '../inputs/InputSelectOrUploadMedia.vue';
import InputWsiwyg from '../inputs/InputWsiwyg.vue';

export default {
    extends: BaseModal,
    props: ['isContentOnly'],
    data() {
        return {
            modalName: 'editExperienceModal',
            contentId: null,
            formData: {organization: {}},
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
            }
        }
    },
    inheritAttrs: false,
    components: {BaseModal, InputMonthYear, InputSelectize, InputSelectOrUploadMedia, InputWsiwyg},
    methods: {

    },
}
</script>