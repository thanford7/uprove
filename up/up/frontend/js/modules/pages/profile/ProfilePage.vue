<template>
    <BasePage>
        <div class="row">
            <CandidateSideBar :user="initData.user" :isOwner="initData.isOwner" :profilePicture="initData.profilePicture"/>
            <div class="col-md-6 ms-md-2">
                <div
                    v-for="(section, idx) in initData.sections"
                    class="card-custom card-custom--no-padding card-custom--no-side-margin card-custom--no-top-margin
                     -border-bottom--light mb-3"
                >
                    <div class="card-custom_body">
                        <div class="row ps-3 pe-3">
                            <div class="col-12">
                                <h5
                                    :data-idx="idx"
                                    :id="`section-${idx}`"
                                    class="d-inline-block section"
                                >{{capitalize(section.sectionType)}}</h5>
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
            <div v-if="!isMobile" class="col-md-2">
                <div class="card-custom card-custom--no-side-margin card-custom--no-top-margin sticky-top section-nav">
                    <h6>Sections</h6>
                    <a
                        v-for="(section, idx) in initData.sections"
                        class="nav-link" :data-idx="idx" :href="`#section-${idx}`"
                    >{{capitalize(section.sectionType)}}</a>
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
import BasePage from "../base/BasePage";
import dataUtil from "../../../utils/data";

export default {
    components: {
        BasePage,
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
    mounted() {
        const sections$ = $('.section');
        const sectionObserver = new IntersectionObserver((entries) => {
            const targetEl = dataUtil.findTopVisibleElement(sections$);
            if (!targetEl) {
                return;
            }
            const targetIdx = $(targetEl).data('idx');
            console.log(targetIdx);
            $('.section-nav a').each((idx, sectionNavItem) => {
                const sectionNavItem$ = $(sectionNavItem);
                console.log(sectionNavItem$.data('idx') === targetIdx);
                sectionNavItem$.toggleClass('active-section', sectionNavItem$.data('idx') === targetIdx);
            });
        }, {
            threshold: 1.0
        });
        sections$.each((idx, s) => {
            sectionObserver.observe(s);
        })
    }
}
</script>