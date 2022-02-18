<template>
    <BaseModal
        modalId="editProfileModal"
        modalTitle="Edit profile"
        @saveChange="saveChange"
    >
        <div class="mb-3">
            <label for="formProfileName" class="form-label">Name</label>
            <input type="text" class="form-control" placeholder="Add name..." id="formProfileName" v-model="formData.profileName">
        </div>
        <div class="mb-3">
            <label class="form-label">Profile picture</label>
            <InputOrViewMedia
                :inputId="getNewElUid()"
                :mediaTypes="[contentTypes.IMAGE]"
                itemLabel="profile picture"
                :currentItem="formData?.profilePicture?.image"
                :isUploadDefault="!formData.profilePicture"
                @selectedMediaNew="formData.newProfilePicture = $event"
            />
        </div>
    </BaseModal>
</template>
<script>
import {CONTENT_TYPES} from '../../globalData';
import BaseModal from './BaseModal.vue';
import InputOrViewMedia from "../inputs/InputOrViewMedia";

export default {
    extends: BaseModal,
    data() {
        return {
            modalName: 'editProfileModal',
            crudUrl: 'user-profile/',
            isUpdateData: true,
            mediaFields: ['newProfilePicture'],
            requiredFields: {
                profileName: '#formProfileName'
            },
            contentTypes: CONTENT_TYPES
        }
    },
    inheritAttrs: false,
    components: {BaseModal, InputOrViewMedia},
}
</script>