<template>
    <BaseModal
        :modalId="modalName"
        modalTitle="Add content"
        :isLargeDisplay="true"
        @saveChange="saveChange"
    >
        <div class="btn-group mb-3" role="group">
            <input type="radio" class="btn-check" name="btnradio"
                   id="btnradio1" autocomplete="off" checked
                   @change="toggleContentType($event, contentTypes.EXISTING)"
            >
            <label class="btn btn-outline-dark" for="btnradio1">Existing content</label>

            <input type="radio" class="btn-check" name="btnradio"
                   id="btnradio2" autocomplete="off"
                   @change="toggleContentType($event, contentTypes.EXPERIENCE)"
            >
            <label class="btn btn-outline-dark" for="btnradio2">New work experience</label>

            <input type="radio" class="btn-check" name="btnradio"
                   id="btnradio3" autocomplete="off"
                   @change="toggleContentType($event, contentTypes.PROJECT)"
            >
            <label class="btn btn-outline-dark" for="btnradio3">New project</label>

            <input type="radio" class="btn-check" name="btnradio"
                   id="btnradio4" autocomplete="off"
                   @change="toggleContentType($event, contentTypes.VIDEO)"
            >
            <label class="btn btn-outline-dark" for="btnradio4">New video</label>
        </div>
        <div v-if="addContentType === contentTypes.EXISTING">
            <label for="selectContent" class="form-label">Existing content</label>
            <ContentSelectize :section="formData" :content="initData.assets"
                              @selected="formData.selectedContentId = $event"/>
        </div>
        <EditMediaModal v-if="[contentTypes.VIDEO, contentTypes.PROJECT].includes(addContentType)"
                          :contentType="addContentType"
                            :isContentOnly="true"
                          ref="formContentMedia"/>
        <EditExperienceModal v-if="addContentType === contentTypes.EXPERIENCE" ref="formContentExperience"
                             :isContentOnly="true"/>
    </BaseModal>
</template>
<script>
import BaseModal from './BaseModal.vue';
import ContentSelectize from '../inputs/ContentSelectize.vue';
import EditExperienceModal from "./EditExperienceModal";
import EditMediaModal from "./EditMediaModal";
import InputSelectize from '../inputs/InputSelectize.vue';

const contentTypes = {
    EXISTING: 'existing',
    EXPERIENCE: 'experience',
    VIDEO: 'video',
    PROJECT: 'project'
}

export default {
    extends: BaseModal,
    components: {BaseModal, ContentSelectize, EditExperienceModal, EditMediaModal, InputSelectize},
    inheritAttrs: false,
    data() {
        return {
            modalName: 'addContentModal',
            crudUrl: 'user-profile/content-item/',
            addContentType: contentTypes.EXISTING,
            contentTypes
        }
    },
    methods: {
        toggleContentType(e, contentType) {
            if ($(e.currentTarget).prop('checked')) {
                this.addContentType = contentType;
            } else {
                this.addContentType = null;
            }
        }
    }
}
</script>
