<template>
    <BasePage>
        <div class="row">
            <CandidateSideBar :user="initData.user" :isOwner="initData.isOwner" :profilePicture="initData.profilePicture"/>
            <div class="col-md-8">
                <div v-for="(section, idx) in initData.sections" class="row card-custom -border-bottom--light mb-2 pb-2 ">
                    <div class="col-12">
                        <h5 class="d-inline-block">{{capitalize(section.sectionType)}}</h5>
                        <button
                            v-if="initData.isOwner" type="button"
                            class="btn btn-sm btn-outline-dark ms-2"
                            @click="eventBus.emit('open:addContentModal', {sectionId: section.id, contentType: getContentType(section.sectionType)})"
                        >
                            <i class="fas fa-plus"></i> Add {{getContentType(section.sectionType)}}
                        </button>
                        <div class="row mt-2 justify-content-center">
                            <ContentCard
                                v-for="sectionItem in section.sectionItems"
                                :contentItem="sectionItem"
                                :contentSection="section"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </BasePage>
    <AddContentModal/>
    <EditEducationModal/>
    <EditExperienceModal/>
    <EditProfileModal/>
    <EditMediaModal/>
    <EditUserProjectModal/>
    <DisplayContentModal/>
</template>
<script>
import AddContentModal from '../../modals/AddContentModal.vue';
import BannerAlert from "../../components/BannerAlert";
import CandidateSideBar from "./CandidateSideBar";
import ContentCard from "./ContentCard.vue"
import DisplayContentModal from '../../modals/DisplayContentModal.vue';
import EditEducationModal from '../../modals/EditEducationModal.vue';
import EditExperienceModal from '../../modals/EditExperienceModal.vue';
import EditProfileModal from '../../modals/EditProfileModal.vue';
import EditMediaModal from '../../modals/EditMediaModal.vue';
import EditUserProjectModal from "../../modals/EditUserProjectModal";
import BasePage from "../base/BasePage";
import dataUtil from "../../../utils/data";

export default {
    components: {
        BasePage,
        EditUserProjectModal,
        AddContentModal,
        BannerAlert,
        CandidateSideBar,
        ContentCard,
        DisplayContentModal,
        EditEducationModal,
        EditExperienceModal,
        EditProfileModal,
        EditMediaModal,
    },
    methods: {
        capitalize: dataUtil.capitalize,
        getContentType: function(sectionType) {
            sectionType = sectionType.toLowerCase()
            if (sectionType === 'projects') {
                return 'project';
            }
            return sectionType;
        }
    },
}
</script>