<template>
    <BaseModal
        :modalId="modalName"
        :isReadOnly="true"
        :modalTitle="cardTitle"
        :isFooterHidden="true"
        :isScrollable="true"
        :isLargeDisplay="true"
    >
        <template v-if="contentItem.type === contentTypes.CUSTOM">
            <div class="mb-3" v-for="section in contentItem.sections">
                <template v-if="section.item">
                    <video v-if="section.item.type === contentTypes.VIDEO" controls :src="section.item.video" @resize="$emit('contentUpdated')"></video>
                    <img v-else-if="section.item.type === contentTypes.IMAGE" :src="section.item.image">
                    <FileDisplay
                        v-else-if="section.item.type === contentTypes.FILE"
                        :file="section.item"
                    />
                </template>
                <div v-else v-html="section.text"></div>
            </div>
        </template>
        <template v-if="contentItem.type === contentTypes.EDUCATION">
            <div class="row">
                <div class="col-2">
                    <img :src="contentItem.school.logo">
                </div>
                <div class="col-10">
                    {{contentItem.degree}}<br>
                    {{contentItem.degreeSubject}}<br>
                    <template v-if="contentItem.startDate">
                        {{formatDate(contentItem.startDate)}} to {{formatDate(contentItem.endDate) || 'current'}}
                    </template>
                    <div v-if="contentItem.activities">
                        Activities:<br>
                        <div v-html="contentItem.activities"></div>
                    </div>
                </div>
            </div>
        </template>
        <template v-if="contentItem.type === contentTypes.CERTIFICATION">
            <div class="row">
                <div class="col-2">
                    <img :src="contentItem.organization.logo">
                </div>
                <div class="col-10">
                    <div>{{contentItem.title}}</div>
                    <div>Issued: {{formatDate(contentItem.issueDate)}}</div>
                    <div v-if="contentItem.hasExpiration">Expires: {{formatDate(contentItem.expirationDate)}}</div>
                </div>
            </div>
        </template>
        <template v-if="contentItem.type === contentTypes.EXPERIENCE">
            <div class="row">
                <div class="col-2">
                    <img :src="contentItem.organization.logo">
                </div>
                <div class="col-10">
                    {{contentItem.positionTitle}}<br>
                    {{contentItem.employmentType}}<br>
                    {{formatDate(contentItem.startDate)}} to {{formatDate(contentItem.endDate) || 'current'}}
                    <div v-html="contentItem.description"></div>
                </div>
            </div>
        </template>
        <template v-if="contentItem.type === contentTypes.PROJECT">
                <BadgesSkillLevels :skillLevels="contentItem.customProject.skillLevels"/>
                <BadgesSkills :skills="contentItem.customProject.skills"/>
                <div id="projectInfo" class="accordion mb-3 mt-3">
                    <AccordionItem accordionElId="projectInfo" :elId="getNewElUid()" :isOpen="false" :isAllowMultipleOpen="true">
                        <template v-slot:header>
                            Project description
                        </template>
                        <template v-slot:body>
                            <div v-html="contentItem.customProject.projectDescription"></div>
                        </template>
                    </AccordionItem>
                    <AccordionItem accordionElId="projectInfo" :elId="getNewElUid()" :isOpen="false" :isAllowMultipleOpen="true">
                        <template v-slot:header>
                            Project background
                        </template>
                        <template v-slot:body>
                            <div v-html="contentItem.customProject.projectBackground"></div>
                        </template>
                    </AccordionItem>
                </div>
                <template v-for="video in contentItem.videos">
                    <video controls :src="video.video"></video>
                </template>
                <template v-for="image in contentItem.images">
                    <img :src="image.image">
                </template>
                <div v-for="file in contentItem.files">
                    <FileDisplay :file="file" :isPreventDownload="!isEmployer && !initData.isOwner"/>
                </div>
        </template>
    </BaseModal>
</template>
<script>
import {CONTENT_TYPES} from '../../globalData';
import AccordionItem from "../components/AccordionItem";
import BadgesSkillLevels from "../components/BadgesSkillLevels";
import BadgesSkills from "../components/BadgesSkills";
import BaseModal from './BaseModal.vue';
import dataUtil from '../../utils/data';
import contentUtil from "../../utils/content";
import FileDisplay from "../components/FileDisplay";

export default {
    extends: BaseModal,
    components: {BaseModal, AccordionItem, BadgesSkillLevels, BadgesSkills, FileDisplay},
    inheritAttrs: false,
    data() {
        return {
            modalName: 'displayContentModal',
            contentTypes: CONTENT_TYPES,
        }
    },
    computed: {
        cardTitle() {
            return contentUtil.getContentTitle(this.contentItem);
        },
        contentItem() {
            return this.formData
        }
    },
    methods: {
        formatDate(dateVal) {
            return dataUtil.formatDate(dateVal, {dateFormat: dataUtil.shorthandDateFormat, isReturnNull: true});
        }
    },
}
</script>