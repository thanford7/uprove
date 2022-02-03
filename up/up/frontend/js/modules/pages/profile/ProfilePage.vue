<template>
    <div class="container-lg">
        <BannerRow/>

        <div v-for="(section, idx) in initData.sections" class="row -border-bottom--light mb-2 pb-2 ">
            <div class="col-12">
                <template>
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
                </template>
                <h4 class="d-inline-block">{{section.title}}</h4>
                <div v-if="initData.isOwner" class="d-inline-block -no-horizontal-padding">
                    <button type="button" class="btn btn-sm btn-outline-secondary" @click="eventBus.emit('open:addContentModal', 'section', idx)">
                        <i class="fas fa-plus"></i> Add card
                    </button>
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
            <button v-if="initData.isOwner" type="button" class="btn btn-sm btn-outline-secondary" @click="eventBus.emit('open:addSectionModal')">
                <i class="fas fa-plus"></i> Add section
            </button>
        </div>

        <AddContentModal/>
        <AddSectionModal/>
        <EditEducationModal/>
        <EditExperienceModal/>
        <EditProfileModal/>
        <EditMediaModal/>
        <DisplayContentModal/>
    </div>
</template>
<script>
import {mapState} from 'vuex';
import BannerRow from "./BannerRow.vue";
import AddContentModal from '../../modals/AddContentModal.vue';
import AddSectionModal from '../../modals/AddSectionModal.vue';
import ContentCard from "./ContentCard.vue"
import DisplayContentModal from '../../modals/DisplayContentModal.vue';
import EditEducationModal from '../../modals/EditEducationModal.vue';
import EditExperienceModal from '../../modals/EditExperienceModal.vue';
import EditProfileModal from '../../modals/EditProfileModal.vue';
import EditMediaModal from '../../modals/EditMediaModal.vue';

export default {
    components: {
        BannerRow,
        AddContentModal,
        AddSectionModal,
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