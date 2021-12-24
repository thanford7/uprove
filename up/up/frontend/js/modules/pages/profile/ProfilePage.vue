<template>
    <div>
        <BannerRow/>

        <div v-for="(section, idx) in profile.sections" :key="`section-${idx}`" class="row -border-bottom--light mb-2 pb-2 ">
            <div class="col-12">
                <template>
                    <i
                        v-if="!(idx === 0)"
                        @click="move(-1, idx)"
                        class="fas fa-arrow-up"
                        title="Move section up"
                    />
                    <i
                        v-if="!(idx === profile.sections.length - 1)"
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
                <div v-if="isOwner" class="d-inline-block -no-horizontal-padding">
                    <button type="button" class="btn btn-sm btn-outline-secondary" @click="eventBus.$emit('open:addContentModal', 'section', idx)">
                        <i class="fas fa-plus"></i> Add card
                    </button>
                </div>

                <div class="row grid">
                    <ContentCard
                        v-for="(contentId, itemIdx) in section.ids"
                        :key="`section-${idx}-${contentId}`"
                        contentSection="section"
                        :contentSectionOrder="idx"
                        :contentItemOrder="itemIdx"
                        :isFirstItem="itemIdx === 0"
                        :isLastItem="itemIdx === section.ids.length - 1"
                        :contentId="contentId"
                    />
                </div>
            </div>
        </div>

        <div class="row mb-2 pb-2 ">
            <button v-if="isOwner" type="button" class="btn btn-sm btn-outline-secondary" @click="eventBus.$emit('open:addSectionModal')">
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
    computed: mapState({
        eventBus: 'eventBus',
        isOwner: 'isOwner',
        profile: 'profile'
    }),
    methods: {
        // Vue and Jquery events don't play well together. This includes bootstrap's modal events
        // We can't listen for bootstrap events like 'show.bs.modal' so instead we watch for the change
        // of any modal to include the "show" class
        watchModals() {
            // Select the node that will be observed for mutations
            const modals$ = $('.modal');

            // Options for the observer (which mutations to observe)
            const config = {attributes: true};

            // Callback function to execute when mutations are observed
            const callback = function(mutationsList, observer) {
                // Use traditional 'for loops' for IE 11
                for(const {attributeName, target} of mutationsList) {
                    if (attributeName  === 'class') {
                        if($(target).hasClass('show')) {
                            $('#site-header').toggle(false);
                        } else {
                            $('#site-header').toggle(true);
                        }
                    }
                }
            };

            // Create an observer instance linked to the callback function
            const observer = new MutationObserver(callback);

            // Start observing the target node for configured mutations
            modals$.each((idx, targetNode) => {
                observer.observe(targetNode, config);
            });
        },
        removeSection(sectionIdx) {
            this.$store.commit('removeSection', sectionIdx);
        },
        move(direction, sectionIdx) {
            this.$store.commit('moveSection', {direction, sectionIdx})
        }
    },
    mounted() {
        this.watchModals();
    }
}
</script>