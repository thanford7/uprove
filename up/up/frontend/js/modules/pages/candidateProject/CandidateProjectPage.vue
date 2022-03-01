<template>
    <div class="container-lg">
        <BannerAlert/>
        <PageHeader title="Project"/>
        <div class="row">
            <CandidateSideBar :user="initData.user" :profilePicture="initData.user.profileImage"/>
            <div class="col-md-8">
                <ProjectDetailAccordion :userProject="initData.userProject"/>
                <div v-if="initData.userProject.projectNotes" class="custom-card">
                    <div v-html="initData.userProject.projectNotes"></div>
                </div>
                <div class="row">
                    <div v-for="file in allFiles" class="col-md-6">
                        <video v-if="file.type === CONTENT_TYPES.VIDEO" controls :src="file.video"></video>
                        <img v-else-if="file.type === CONTENT_TYPES.IMAGE" :src="file.image">
                        <FileDisplay v-else :file="file" :isPreventDownload="!isEmployer && !isAdmin"/>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import {CONTENT_TYPES} from '../../../globalData';
import BannerAlert from "../../components/BannerAlert";
import CandidateSideBar from "../profile/CandidateSideBar";
import FileDisplay from "../../components/FileDisplay";
import PageHeader from "../../components/PageHeader";
import ProjectDetailAccordion from "../../components/ProjectDetailAccordion";

export default {
    name: "CandidateProjectPage",
    components: {BannerAlert, CandidateSideBar, FileDisplay, PageHeader, ProjectDetailAccordion},
    data() {
        return {
            CONTENT_TYPES
        }
    },
    computed: {
        allFiles() {
            const p = this.initData.userProject
            return [...p.videos, ...p.images, ...p.files]
        }
    }
}
</script>