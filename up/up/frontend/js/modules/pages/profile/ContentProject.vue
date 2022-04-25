<template>
    <div class="pb-1">
        <BadgesSkillLevels :skillLevels="contentItem.customProject.skillLevels"/>
        <BadgesSkills :skills="contentItem.customProject.skills"/>
        <div class="mt-2 mb-1">
            <div v-html="contentItem.customProject.projectDescription"></div>
        </div>
        <div class="row">
            <div v-for="video in contentItem.videos" class="col-md-4">
                <h6>{{ video.title }}</h6>
                <video controls :src="video.video"></video>
            </div>
            <div v-for="image in contentItem.images" class="col-md-4">
                <h6>{{ image.title }}</h6>
                <img class="img-150" :src="image.image">
            </div>
        </div>
        <div>
            <template v-for="file in contentItem.files">
                <FileDisplay :file="file" :isPreventDownload="!isEmployer && !initData.isOwner"/>
            </template>
        </div>
    </div>
</template>

<script>
import BadgesSkillLevels from "../../components/BadgesSkillLevels";
import BadgesSkills from "../../components/BadgesSkills";
import FileDisplay from "../../components/FileDisplay";
import form from "../../../utils/form";
import skillLevels from "../../selectizeCfgs/skillLevels";

export default {
    name: "ContentProject",
    components: {BadgesSkillLevels, BadgesSkills, FileDisplay},
    props: {
        contentItem: Object
    },
    methods: {
        hasText(text) {
            return !form.isEmptyWysiwyg(text);
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
    }
}
</script>