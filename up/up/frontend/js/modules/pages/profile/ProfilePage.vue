<template>
    <div class="container-lg mt-3">
        <BannerAlert/>
        <div class="row">
            <div class="col-md-3 col-12 card-custom">
                <div class="profile-picture">
                    <span id="profilePic">
                        <img v-if="initData.profilePicture" :src="initData.profilePicture" alt="Profile picture">
                        <i v-else class="fas fa-user fa-4x"></i>
                        <i
                            v-if="initData.isOwner"
                            class="fas fa-pencil-alt"
                            id="editProfile"
                            @click="eventBus.emit('open:editProfileModal')"
                        />
                    </span>
                    <h4 class="-text-center mt-2">{{initData.firstName}} {{initData.lastName}}</h4>
                </div>
            </div>
            <div class="col-md-8 col-12">
                <div v-for="(section, idx) in initData.sections" class="row card-custom -border-bottom--light mb-2 pb-2 ">
                    <div class="col-12">
                        <h4 class="d-inline-block">{{section.title}}</h4>
                        <button v-if="initData.isOwner" type="button" class="btn btn-sm btn-outline-dark ms-2" @click="eventBus.emit('open:addContentModal', section)">
                            <i class="fas fa-plus"></i> Add card
                        </button>
                        <div class="-float-right">
                            <i
                                v-if="!(idx === 0)"
                                @click="move(-1, idx)"
                                class="fas fa-arrow-up"
                                title="Move section up"
                            />
                            <i
                                v-if="!(idx === initData.sections.length - 1)"
                                @click="move(1, idx)"
                                class="fas fa-arrow-down"
                                title="Move section down"
                            />
                            <i
                                @click="removeSection(idx)"
                                class="fas fa-trash"
                                title="Remove section"
                            />
                        </div>

                        <div class="row grid">
                            <ContentCard
                                v-for="(sectionItem, itemIdx) in section.sectionItems"
                                contentSection="section"
                                :contentSectionOrder="idx"
                                :contentItemOrder="itemIdx"
                                :isFirstItem="itemIdx === 0"
                                :isLastItem="itemIdx === section.ids.length - 1"
                                :contentItem="sectionItem.item"
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

        <AddContentModal/>
        <AddSectionModal/>
<!--        <EditEducationModal/>-->
<!--        <EditExperienceModal/>-->
<!--        <EditProfileModal/>-->
<!--        <EditMediaModal/>-->
<!--        <DisplayContentModal/>-->
    </div>
</template>
<script>
import AddContentModal from '../../modals/AddContentModal.vue';
import AddSectionModal from '../../modals/AddSectionModal.vue';
import BannerAlert from "../../components/BannerAlert";
import ContentCard from "./ContentCard.vue"
import DisplayContentModal from '../../modals/DisplayContentModal.vue';
import EditEducationModal from '../../modals/EditEducationModal.vue';
import EditExperienceModal from '../../modals/EditExperienceModal.vue';
import EditProfileModal from '../../modals/EditProfileModal.vue';
import EditMediaModal from '../../modals/EditMediaModal.vue';

export default {
    components: {
        AddContentModal,
        AddSectionModal,
        BannerAlert,
        ContentCard,
        DisplayContentModal,
        EditEducationModal,
        EditExperienceModal,
        EditProfileModal,
        EditMediaModal
    },
    methods: {
        removeSection(sectionIdx) {
            this.$store.commit('removeSection', sectionIdx);
        },
        move(direction, sectionIdx) {
            this.$store.commit('moveSection', {direction, sectionIdx})
        }
    },
}
</script>