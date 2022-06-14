<template>
    <BasePage>
        <div class="row justify-content-center">
            <CandidateSideBar
                :user="initData.user"
                :isOwner="initData.isOwner"
                :profilePicture="initData.profilePicture"
                :profileId="initData.id"
                :applications="initData.applications"
            />
            <div class="col-md-6 ms-md-2">
                <div
                    v-if="completedCourses.length || initData.isOwner"
                    class="card-custom card-custom--no-padding card-custom--no-side-margin card-custom--no-top-margin
                     -border-bottom--light mb-3"
                >
                    <div class="card-custom_body">
                        <div class="row ps-3 pe-3">
                            <div class="col-12">
                                <h5
                                    data-idx="0"
                                    id="section-0"
                                    class="d-inline-block section"
                                >Certifications</h5>
                                <a
                                    v-if="initData.isOwner" type="button"
                                    class="btn btn-sm btn-outline-dark ms-2"
                                    href="/courses/"
                                >
                                    Find courses
                                </a>
                                <div class="row mt-2">
                                    <div v-for="course in completedCourses" class="col-md-6 col-12 mb-3">
                                        <div class="certification">
                                            <div class="row">
                                                <div class="col-3 d-flex align-items-center">
                                                    <img :src="course.courseData.certificateImage" alt="Course image">
                                                </div>
                                                <div class="col-9">
                                                    {{ course.courseData.title }}
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div v-if="!completedCourses.length" class="row mt-2 blank-section">
                                    <div class="col-1">
                                        <i class="fas fa-lightbulb fa-2x -color-yellow-text"></i>
                                    </div>
                                    <div class="col-11">
                                        <span>Courses allow you to demonstrate your Customer Success skills to employers.</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div
                    v-for="(section, idx) in initData.sections"
                    class="card-custom card-custom--no-padding card-custom--no-side-margin card-custom--no-top-margin
                     -border-bottom--light mb-3"
                >
                    <div class="card-custom_body">
                        <div class="row ps-3 pe-3">
                            <div class="col-12">
                                <h5
                                    :data-idx="idx + 1"
                                    :id="`section-${idx + 1}`"
                                    class="d-inline-block section"
                                >{{capitalize(section.sectionType)}}</h5>
                                <button
                                    v-if="initData.isOwner" type="button"
                                    class="btn btn-sm btn-outline-dark ms-2"
                                    @click="eventBus.emit('open:addContentModal', {sectionId: section.id, contentType: getContentType(section.sectionType)})"
                                >
                                    <i class="fas fa-plus"></i> Add {{getContentType(section.sectionType)}}
                                </button>
                                <div v-if="section.sectionItems.length" class="row mt-2 justify-content-center">
                                    <ContentCard
                                        v-for="(sectionItem, idx) in section.sectionItems.slice(0,contentItemLimit)"
                                        :class="(idx !== contentItemLimit - 1) ? 'mb-4' : ''"
                                        :contentItem="sectionItem"
                                        :contentSection="section"
                                    />
                                </div>
                                <div v-else-if="isSelf(initData?.user?.id)" class="row mt-2 blank-section">
                                    <div class="col-1">
                                        <i class="fas fa-lightbulb fa-2x -color-yellow-text"></i>
                                    </div>
                                    <div class="col-11">
                                        <span v-if="section.sectionType === PROFILE_SECTIONS.PROJECTS">
                                            Projects are another great way to demonstrate your skill set. Make sure your profile stands out by adding your first project.
                                        </span>
                                        <span v-if="section.sectionType === PROFILE_SECTIONS.EXPERIENCE">
                                            While Uprove emphasizes your projects and courses, your past experience is also important
                                            to employers. Show off what you've accomplished!
                                        </span>
                                        <span v-if="section.sectionType === PROFILE_SECTIONS.EDUCATION">
                                            Education rounds out the picture for employers. Formal training is a good indicator
                                            that you are passionate and knowledgeable about a certain subject area.
                                        </span>
                                    </div>
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
                        class="nav-link" data-idx="0" href="#section-0"
                        @click="selectSection"
                    >Certifications</a>
                    <a
                        v-for="(section, idx) in initData.sections"
                        class="nav-link" :data-idx="idx + 1" :href="`#section-${idx + 1}`"
                        @click="selectSection"
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
import {PROFILE_SECTIONS} from '../../../globalData';
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
    computed: {
        completedCourses() {
            return this.initData.user.courses.reduce((completedCourses, course) => {
                if (!course.completedDateTime) {
                    return completedCourses;
                }
                course.courseData = this.initData.courses.find((c) => c.id === course.courseId);
                completedCourses.push(course);
                return completedCourses;
            }, []);
        }
    },
    data() {
        return {
            contentItemLimit: 2,
            PROFILE_SECTIONS
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
        },
        selectSection(e) {
            const sectionItemIdx = $(e.currentTarget).data('idx');
            this.toggleSections(sectionItemIdx);
        },
        toggleSections(targetIdx) {
            $('.section-nav a').each((idx, sectionNavItem) => {
                const sectionNavItem$ = $(sectionNavItem);
                sectionNavItem$.toggleClass('active-section', sectionNavItem$.data('idx') === targetIdx);
            });
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
            this.toggleSections(targetIdx);
        }, {
            threshold: 1.0
        });
        sections$.each((idx, s) => {
            sectionObserver.observe(s);
        })
    }
}
</script>