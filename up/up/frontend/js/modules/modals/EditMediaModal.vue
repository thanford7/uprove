<template>
    <BaseModal
        :modalId="modalName"
        :modalTitle="`Edit ${contentType}`"
        :isLargeDisplay="true"
        :isContentOnly="isContentOnly"
        @saveChange="saveChange"
    >
        <div class="mb-3">
            <label for="formContentTitle" class="form-label">Title</label>
            <input type="text" class="form-control" placeholder="Add title..." id="formContentTitle" v-model="formData.title">
        </div>
        <div class="mb-3">
            <label class="form-label">Banner {{allowedBannerMediaTypes.join(' or ')}}</label>
            <InputSelectOrUploadMedia
                ref="mediaInput"
                :mediaTypes="allowedBannerMediaTypes"
                :isMultiUpload="false"
            />
        </div>
        <div class="mb-3">
            <label class="form-label">Description</label>
            <InputWsiwyg placeholder="Add a description..." v-model="formData.description"/>
        </div>
        <div v-if="contentType === 'project'" class="mb-3">
            <label class="form-label">Files</label>
            <InputSelectOrUploadMedia
                ref="fileInput"
                :mediaTypes="['file']"
                :isMultiUpload="true"
            />
        </div>
    </BaseModal>
</template>
<script>
import BaseModal from './BaseModal.vue';
import InputSelectOrUploadMedia from '../inputs/InputSelectOrUploadMedia.vue';
import InputWsiwyg from '../inputs/InputWsiwyg.vue';

export default {
    extends: BaseModal,
    data() {
        return {
            modalName: 'editMediaModal',
            contentId: null,
        }
    },
    inheritAttrs: false,
    props: ['isContentOnly', 'contentType'],
    components: {BaseModal, InputSelectOrUploadMedia, InputWsiwyg},
    computed: {
        allowedBannerMediaTypes() {
            return (this.contentType === 'video') ? ['video'] : ['video', 'image'];
        }
    },
}
</script>