<template>
    <BaseModal
        :modalId="modalName"
        :modalTitle="getModalTitle()"
        :isLargeDisplay="true"
    >
        <div v-if="!isEmptyString(formData.projectNotes)" class="mb-3">
            <label class="form-label">Notes</label>
            <div v-html="formData.projectNotes"></div>
        </div>
        <div v-if="formData.files && formData.files.length" class="mb-3">
            <label class="form-label">Files</label>
            <div v-for="file in formData.files">
                <FileDisplay :file="file"/>
            </div>
        </div>
        <div v-if="formData.videos && formData.videos.length" class="mb-3">
            <label class="form-label">Videos</label>
            <div v-for="video in formData.videos">
                <video controls>
                  <source :src="video.video">
                </video>
            </div>
        </div>
        <div v-if="formData.images && formData.images.length" class="mb-3">
            <label class="form-label">Images</label>
            <div v-for="image in formData.images">
                <img :src="image.image" class="img-thumbnail">
            </div>
        </div>
    </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal";
import dataUtil from "../../utils/data";
import FileDisplay from "../components/FileDisplay";
import formChecker from '../../utils/form';

export default {
    name: "ViewCandidateApplicationModal",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal, FileDisplay},
    data() {
        return {
            modalName: 'viewCandidateApplicationModal',
        }
    },
    methods: {
        isEmpty: dataUtil.isEmpty,
        isEmptyString: formChecker.isEmptyWysiwyg,
        getModalTitle() {
            if (!this.formData || this.isEmpty(this.formData)) {
                return '';
            }
            return `Application: ${this.formData.user.firstName} ${this.formData.user.lastName}`;
        }
    }
}
</script>