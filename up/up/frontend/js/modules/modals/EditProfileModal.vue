<template>
    <BaseModal
        modalId="editProfileModal"
        modalTitle="Edit profile"
        :isLargeDisplay="true"
        @saveChange="saveChange"
    >
        <template v-if="!isEmptyOrNil(formData)">
            <div class="mb-3">
                <InputOrViewMedia
                    :inputId="getNewElUid()"
                    :mediaTypes="[contentTypes.IMAGE]"
                    itemLabel="profile picture"
                    :currentItem="formData?.profilePicture?.image"
                    :isUploadDefault="!formData.profilePicture"
                    @selectedMediaNew="formData.newProfilePicture = $event"
                />
            </div>
            <div class="mb-3">
                <InputOrViewMedia
                    :inputId="getNewElUid()"
                    :mediaTypes="[contentTypes.FILE]"
                    :supportedFormatsOverride="['doc', 'docx', 'pdf']"
                    itemLabel="resume"
                    :currentItem="formData.user.resume"
                    :isUploadDefault="!formData.user.resume"
                    @selectedMediaNew="formData.newResume = $event"
                />
            </div>
            <LocationInputs :formData="formData.user"/>
            <div class="mb-3">
                <EditUserTagTable ref="userSkills" :userTags="initData.user.skills" :tagType="tagTypes.SKILL"/>
            </div>
            <div class="mb-3">
                <EditUserTagTable ref="userInterests" :userTags="initData.user.interests" :tagType="tagTypes.INTEREST"/>
            </div>
        </template>
    </BaseModal>
</template>
<script>
import {CONTENT_TYPES, SEVERITY, TAG_TYPES} from '../../globalData';
import BaseModal from './BaseModal.vue';
import EditUserTagTable from "../components/EditUserTagTable";
import InputOrViewMedia from "../inputs/InputOrViewMedia";
import LocationInputs from "../inputs/LocationInputs";
import dataUtil from "../../utils/data";

export default {
    extends: BaseModal,
    data() {
        return {
            modalName: 'editProfileModal',
            crudUrl: 'user-profile/',
            isHardRefresh: true,
            mediaFields: new Set(['newProfilePicture', 'newResume']),
            contentTypes: CONTENT_TYPES,
            tagTypes: TAG_TYPES
        }
    },
    inheritAttrs: false,
    components: {BaseModal, EditUserTagTable, InputOrViewMedia, LocationInputs},
    methods: {
        isEmptyOrNil: dataUtil.isEmptyOrNil.bind(dataUtil),
        isGoodFormFields(formData) {
            if(this.$refs.userSkills.hasDuplicate()) {
                this.addPopover($(this.$refs.userSkills.$el),
                {severity: SEVERITY.WARN, content: 'Cannot have the same skill multiple times', isOnce: true}
                );
                return false;
            }
            if(this.$refs.userInterests.hasDuplicate()) {
                this.addPopover($(this.$refs.userInterests.$el),
                {severity: SEVERITY.WARN, content: 'Cannot have the same interest multiple times', isOnce: true}
                );
                return false;
            }
            return true;
        },
        processFormData() {
            const userSkills = this.$refs.userSkills.getTags();
            const userInterests = this.$refs.userInterests.getTags();
            return Object.assign(
                dataUtil.pick(
                    this.readForm(),
                    ['id', 'profilePicture', 'newProfilePicture', 'newResume']
                ),
                dataUtil.pick(this.formData.user, ['city', 'stateId', 'countryId']),
                {userInterests, userSkills}
            );
        },
    }
}
</script>