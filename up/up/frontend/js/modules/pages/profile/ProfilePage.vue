<template>
    <BasePage>
        <div class="row">
            <CandidateSideBar :user="initData.user" :isOwner="initData.isOwner" :profilePicture="initData.profilePicture"/>
            <div class="col-md-8 ms-md-2">
                <div
                    v-for="(section, idx) in initData.sections"
                    class="card-custom card-custom--no-padding card-custom--no-side-margin card-custom--no-top-margin
                     -border-bottom--light mb-3"
                >
                    <div class="card-custom_body">
                        <div class="row ps-3 pe-3">
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
                                        v-for="(sectionItem, idx) in section.sectionItems.slice(0,contentItemLimit)"
                                        :class="(idx !== contentItemLimit - 1) ? 'mb-4' : ''"
                                        :contentItem="sectionItem"
                                        :contentSection="section"
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                    <div
                        v-if="section.sectionItems.length > contentItemLimit"
                        class="btn btn-outline-secondary btn-flat-top w-100 -color-darkgrey-text"
                        style="font-weight: 600"
                        @click="contentItemLimit = section.sectionItems.length"
                    >
                        View {{pluralize(
                            `additional ${getPluralizeContentType(section.sectionType)}`,
                        section.sectionItems.length - contentItemLimit
                        )}}
                    </div>
                </div>
            </div>
        </div>
    </BasePage>
    <template v-if="initData.isOwner">
        <AddContentModal/>
        <EditEducationModal/>
        <EditExperienceModal/>
        <EditProfileModal/>
        <EditMediaModal/>
        <EditUserProjectModal/>
    </template>
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
    data() {
        return {
            contentItemLimit: 2
        }
    },
    methods: {
        capitalize: dataUtil.capitalize,
        getContentType: function(sectionType) {
            sectionType = sectionType.toLowerCase()
            if (sectionType === 'projects') {
                return 'project';
            }
            return sectionType;
        },
        getPluralizeContentType: function(sectionType) {
            const type = this.getContentType(sectionType);
            if (type === 'education') {
                return 'education item';
            }
            return type;
        }
    },
}
</script>