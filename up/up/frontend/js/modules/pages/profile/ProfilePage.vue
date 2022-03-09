<template>
    <BasePage>
        <div class="row">
            <CandidateSideBar :user="initData.user" :isOwner="initData.isOwner" :profilePicture="initData.profilePicture"/>
            <div class="col-md-8">
                <div v-for="(section, idx) in initData.sections" class="row card-custom -border-bottom--light mb-2 pb-2 ">
                    <div class="col-12">
                        <h4 class="d-inline-block">{{section.title}}</h4>
                        <button v-if="initData.isOwner" type="button" class="btn btn-sm btn-outline-dark ms-2" @click="eventBus.emit('open:addContentModal', {sectionId: section.id})">
                            <i class="fas fa-plus"></i> Add card
                        </button>
                        <div v-if="initData.isOwner" class="-float-right">
                            <i
                                v-if="!(idx === 0)"
                                @click="move(-1, section)"
                                class="fas fa-arrow-up"
                                title="Move section up"
                            />
                            <i
                                v-if="!(idx === initData.sections.length - 1)"
                                @click="move(1, section)"
                                class="fas fa-arrow-down"
                                title="Move section down"
                            />
                            <i
                                @click="removeSection(section)"
                                class="fas fa-trash"
                                title="Remove section"
                            />
                        </div>

                        <div class="row mt-2 justify-content-center">
                            <ContentCard
                                v-for="sectionItem in section.sectionItems"
                                :contentItem="sectionItem"
                                :contentSection="section"
                            />
                        </div>
                    </div>
                </div>

                <div class="row mb-2 pb-2 ">
                    <button v-if="initData.isOwner" type="button" class="btn btn-sm btn-outline-dark" @click="eventBus.emit('open:addSectionModal')">
                        <i class="fas fa-plus"></i> Add section
                    </button>
                </div>
            </div>
        </div>
    </BasePage>
    <AddContentModal/>
    <AddSectionModal/>
    <EditEducationModal/>
    <EditExperienceModal/>
    <EditProfileModal/>
    <EditMediaModal/>
    <EditUserProjectModal/>
    <DisplayContentModal/>
</template>
<script>
import AddContentModal from '../../modals/AddContentModal.vue';
import AddSectionModal from '../../modals/AddSectionModal.vue';
import BannerAlert from "../../components/BannerAlert";
import CandidateSideBar from "./CandidateSideBar";
import ContentCard from "./ContentCard.vue"
import DisplayContentModal from '../../modals/DisplayContentModal.vue';
import EditEducationModal from '../../modals/EditEducationModal.vue';
import EditExperienceModal from '../../modals/EditExperienceModal.vue';
import EditProfileModal from '../../modals/EditProfileModal.vue';
import EditMediaModal from '../../modals/EditMediaModal.vue';
import InfoToolTip from "../../components/InfoToolTip";
import ProgressPill from "../../components/ProgressPill";
import EditUserProjectModal from "../../modals/EditUserProjectModal";
import BasePage from "../BasePage";

export default {
    data() {
        return {
            crudUrl: 'user-profile/section/',
            isUpdateData: true,
            updateDeleteMethod: 'POST'
        }
    },
    components: {
        BasePage,
        EditUserProjectModal,
        AddContentModal,
        AddSectionModal,
        BannerAlert,
        CandidateSideBar,
        ContentCard,
        DisplayContentModal,
        EditEducationModal,
        EditExperienceModal,
        EditProfileModal,
        EditMediaModal,
        InfoToolTip,
        ProgressPill
    },
    methods: {
        getDeleteConfirmationMessage() {
            return 'Are you sure you want to delete this section? The content will not be deleted and will still be available to add to other sections.'
        },
        readForm() {
            return Object.assign(this.formData, {
                userId: this.initData.user.id,
                profileId: this.initData.id
            });
        },
        removeSection(section) {
            this.formData = section;
            this.deleteObject();
        },
        move(direction, section) {
            section.sectionOrder += direction;
            this.formData = section;
            this.saveChange()
        }
    },
}
</script>