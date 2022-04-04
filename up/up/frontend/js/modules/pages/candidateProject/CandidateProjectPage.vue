<template>
    <BasePage :headerTitle="pageHeader">
        <div class="row">
            <CandidateSideBar :user="initData.user" :profilePicture="initData.user.profileImage"/>
            <div class="col-md-8 card-custom">
                <div>
                    <BadgesSkillLevels :skillLevels="initData.userProject.customProject.skillLevels"/>
                    <BadgesSkills :skills="initData.userProject.customProject.skills"/>
                </div>
                <ProjectDetailAccordion :userProject="initData.userProject"/>
                <div v-if="initData.userProject.projectNotes">
                    <h4>Project notes</h4>
                    <div v-html="initData.userProject.projectNotes"></div>
                </div>
                <div class="row">
                    <div v-for="file in allFiles" class="col-md-6">
                        <video v-if="file.type === CONTENT_TYPES.VIDEO" controls :src="file.video"></video>
                        <img v-else-if="file.type === CONTENT_TYPES.IMAGE" :src="file.image">
                        <FileDisplay v-else :file="file" :isPreventDownload="!isEmployer && !isAdmin && !isSelf(initData.user.id)"/>
                    </div>
                </div>
            </div>
        </div>
    </BasePage>
</template>

<script>
import {CONTENT_TYPES} from '../../../globalData';
import BadgesSkillLevels from "../../components/BadgesSkillLevels";
import BadgesSkills from "../../components/BadgesSkills";
import BannerAlert from "../../components/BannerAlert";
import CandidateSideBar from "../profile/CandidateSideBar";
import FileDisplay from "../../components/FileDisplay";
import PageHeader from "../../components/PageHeader";
import ProjectDetailAccordion from "../../components/ProjectDetailAccordion";
import skillLevelSelectize from "../../selectizeCfgs/skillLevels";
import BasePage from "../base/BasePage";

export default {
    name: "CandidateProjectPage",
    components: {
        BasePage,
        BadgesSkillLevels, BadgesSkills, BannerAlert, CandidateSideBar,
        FileDisplay, PageHeader, ProjectDetailAccordion
    },
    data() {
        return {
            CONTENT_TYPES
        }
    },
    computed: {
        allFiles() {
            const p = this.initData.userProject
            return [...p.videos, ...p.images, ...p.files]
        },
        pageHeader() {
            const cp = this.initData.userProject.customProject
            return `${cp.role}: ${cp.projectTitle}`;
        }
    },
    mounted() {
        skillLevelSelectize.setSkillLevels([this.initData.userProject.customProject], true);
    }
}
</script>