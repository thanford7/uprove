<template>
    <BaseModal
        :modalId="modalName"
        :modalTitle="(formData.id) ? `Edit course: ${formData.title}`: 'Create new course'"
        :primaryButtonText="(formData.id) ? 'Save changes' : 'Create course'"
        :isAllowDelete="Boolean(formData.id)"
        @saveChange="saveChange($event)"
        @deleteObject="deleteObject($event)"
    >
        <div class="mb-3">
            <label for="courseTitle" class="form-label">Title</label>
            <input type="text" class="form-control" placeholder="Required" id="courseTitle" v-model="formData.title">
        </div>
        <div class="mb-3">
            <label for="courseDescription" class="form-label">Short Description</label>
            <textarea
                rows="3" class="form-control"
                placeholder="Description"
                id="courseDescription"
                v-model="formData.shortDescription"
            />
        </div>
        <div class="mb-3">
            <InputOrViewMedia
                inputId="courseImage"
                :mediaTypes="[globalData.CONTENT_TYPES.IMAGE]"
                itemLabel="Cover Image"
                :currentItem="formData.coverImage"
                :isUploadDefault="true"
                @selectedMediaNew="formData.newCoverImage = $event"
            />
        </div>
        <div class="mb-3">
            <InputOrViewMedia
                inputId="certificateImage"
                :mediaTypes="[globalData.CONTENT_TYPES.IMAGE]"
                itemLabel="Certificate Image"
                :currentItem="formData.certificateImage"
                :isUploadDefault="true"
                @selectedMediaNew="formData.newCertificateImage = $event"
            />
        </div>
        <div class="mb-3">
            <label for="courseSalesSlug" class="form-label">Teachable Sales Page Slug</label>
            <input type="text" class="form-control" placeholder="Required" id="courseSalesSlug" v-model="formData.salesPageSlug">
        </div>
        <div class="mb-3">
            <label for="courseTeachableId" class="form-label">Teachable Course ID</label>
            <input type="text" class="form-control" placeholder="Required" id="courseTeachableId" v-model="formData.teachableCourseId">
        </div>
        <div class="mb-3">
            <div id="courseBasicPrice" class="input-group mb-3">
                <span class="input-group-text">$</span>
                <input
                    type="number" min="0" step="5"
                    class="form-control" placeholder="Price" v-model="formData.priceBasic"
                >
            </div>
        </div>
    </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal";
import InputSelectize from "../inputs/InputSelectize";
import InputOrViewMedia from "../inputs/InputOrViewMedia";

export default {
    name: "EditCourseModal",
    extends: BaseModal,
    inheritAttrs: false,
    components: {InputOrViewMedia, BaseModal, InputSelectize},
    data() {
        return {
            modalName: 'editCourseModal',
            crudUrl: 'course/',
            isHardRefresh: true,
            requiredFields: {
                title: '#courseTitle',
                shortDescription: '#courseDescription',
                salesPageSlug: '#courseSalesSlug',
                teachableCourseId: '#courseTeachableId',
                priceBasic: '#courseBasicPrice'
            },
            mediaFields: ['newCoverImage', 'newCertificateImage']
        }
    },
    methods: {
        isGoodFormFields(formData) {
            // Check if image has already been saved or was uploaded
            if (!formData.coverImage && !formData.newCoverImage) {
                this.addPopover($('#courseImage'),
                {severity: SEVERITY.WARN, content: 'Required field', isOnce: true}
                    );
                return false;
            }
            if (!formData.certificateImage && !formData.newCertificateImage) {
                this.addPopover($('#certificateImage'),
                {severity: SEVERITY.WARN, content: 'Required field', isOnce: true}
                    );
                return false;
            }
            return true;
        },
    }
}
</script>