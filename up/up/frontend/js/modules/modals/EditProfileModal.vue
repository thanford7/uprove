<template>
    <BaseModal
        modalId="editProfileModal"
        modalTitle="Edit profile"
        @saveChange="saveChange"
    >
        <div class="mb-3">
            <label for="formProfileName" class="form-label">Name</label>
            <input type="text" class="form-control" placeholder="Add name..." id="formProfileName" v-model="formData.profile_name">
        </div>
        <div class="mb-3">
            <label class="form-label">Profile picture</label>
            <InputSelectOrUploadMedia
                ref="profilePic"
                :currentMediaIds="[profile.profile_picture.ID]"
                :mediaTypes="['image']"
                placeholderDescription="profile picture"
            />
        </div>
    </BaseModal>
</template>
<script>
import Modal from 'bootstrap/js/dist/modal';
import {mapState} from 'vuex';
import BaseModal from './BaseModal.vue';
import InputSelectOrUploadMedia from '../inputs/InputSelectOrUploadMedia.vue';

export default {
    extends: BaseModal,
    data() {
        return {
            modalName: 'editProfileModal',

            inputs: {
                profile_name: {
                    setter: () => this.profile.profile_name
                },
            },
        }
    },
    inheritAttrs: false,
    components: {BaseModal, InputSelectOrUploadMedia},
    computed: {
        ...mapState({
            profile: 'profile',
            profilePicture: 'profilePicture',
            crudUrl: 'crudUrlProfile'
        }),
        formData() {
            const formData = {}
            Object.entries(this.inputs).forEach(([input, cfg]) => {
                formData[input] = cfg.setter();
            });
            return formData;
        }
    },
    methods: {
        onSaveSuccess(requestData, responseData) {
            this.eventBus.loadContent(['profile', 'media'])
        },
        hookEvents() {
            this.eventBus.$on('open:editProfileModal', () => {
                this.modal$.show();
            });
        },
        getPreSaveChange() {
            const {uploadValue, existingValue} = this.$refs.profilePic.getValue();
            if (uploadValue) {
                return this.eventBus.createMediaItem(uploadValue).then((mediaItem) => ({profile_picture: mediaItem.id}));
            } else {
                this.formData.profile_picture = existingValue;
                return this.$super(BaseModal).getPreSaveChange();
            }
        },
        toggleImageUpload(isImageUpload) {
            this.isImageUpload = isImageUpload;
            this.imageToggle$.text((isImageUpload) ? 'Select existing image' : 'Upload new image');
            this.imageUpload$.toggle(isImageUpload);
            this.imageSel$.toggle(!isImageUpload);
        },
    },
    mounted() {
        this.imageSel$ = $(`#formImageSel-${this.profile.ID}`).parent().find('.selectize-control');
        this.imageUpload$ = $(`#formImageUpload-${this.profile.ID}`);
        this.imageToggle$ = $(`#formToggleImageUpload-${this.profile.ID}`);
        this.toggleImageUpload(this.isImageUpload);
    }
}
</script>