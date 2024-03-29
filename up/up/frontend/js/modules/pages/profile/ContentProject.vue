<template>
    <div class="pb-1 mt-2">
        <BadgesSkills :skills="contentItem.customProject.skills"/>
        <div class="mt-2">
            <div class="-color-moderategrey-text" v-html="contentItem.customProject.projectDescription"></div>
        </div>
        <div class="row justify-content-around project-showcase mt-4">
            <span class="badge project-showcase-title -color-lightgrey -color-black-text">Project submission</span>
            <template v-for="file in featuredFiles">
                <div class="col-md-6 col-12 mb-3">
                    <h6 class="text-center project-item-title">
                        <FileDisplay :file="file" :isPreventDownload="!(isEmployer || initData.isOwner)"/>
                    </h6>
                    <div class="project-item d-flex align-items-center justify-content-center">
                        <video v-if="file.type === CONTENT_TYPES.VIDEO" controls :src="file.video"/>
                        <img v-if="file.type === CONTENT_TYPES.IMAGE" :src="file.image" class="project-file-image">
                        <img v-if="file.type === CONTENT_TYPES.FILE" :src="file.thumbnail" class="project-file-image">
                    </div>
                </div>
            </template>
            <div class="col-12" v-if="featuredFiles.length !== allFiles.length">
                <span class="badge -color-lightgrey -color-black-text -text-medium">
                    +{{pluralize('additional file', allFiles.length - featuredFiles.length)}}
                </span>
            </div>
            <div
                class="btn btn-outline-secondary btn-flat-top w-100 mt-3 -color-darkgrey-text"
                style="font-weight: 600"
                @click="redirectUrl(`/user-project/${contentItem.id}/`, true)"
            >
                View full project submission <i class="fas fa-external-link-alt"></i>
            </div>
        </div>
    </div>
</template>

<script>
import {CONTENT_TYPES} from '../../../globalData';
import BadgesSkills from "../../components/BadgesSkills";
import FileDisplay from "../../components/FileDisplay";
import form from "../../../utils/form";
import InfoToolTip from "../../components/InfoToolTip";
import skillLevels from "../../selectizeCfgs/skillLevels";

export default {
    name: "ContentProject",
    components: {BadgesSkills, FileDisplay, InfoToolTip},
    props: {
        contentItem: Object
    },
    computed: {
        allFiles() {
            return [...this.contentItem.videos, ...this.contentItem.images, ...this.contentItem.files];
        },
        featuredFiles() {
            const files = [...this.contentItem.videos, ...this.contentItem.images, ...this.filesWithThumbnails];
            return files.slice(0,2);
        },
        filesWithThumbnails() {
            return this.contentItem.files.filter((f) => f.thumbnail);
        },
    },
    data() {
        return {
            CONTENT_TYPES
        }
    },
    methods: {
        hasText(text) {
            return !form.isEmptyWysiwyg(text);
        },
        setProjectItemHeight() {
            let containerMaxHeight = 0;
            const projectItems = $('.project-item video, .project-item img');
            projectItems.each((idx, el) => {
                const height = $(el).height();
                containerMaxHeight = Math.max(containerMaxHeight, height);
            });
            if (containerMaxHeight === 0) {
                return;
            }
            projectItems.each((idx, el) => {
                $(el).height(containerMaxHeight);
            });
        },
        updateSkillLevels() {
            if (!this.contentItem.customProject.skillLevels) {
                skillLevels.setSkillLevels([this.contentItem.customProject], true);
            }
        }
    },
    mounted() {
        this.updateSkillLevels();
    },
    updated() {
        this.updateSkillLevels();
        this.setProjectItemHeight();
    }
}
</script>