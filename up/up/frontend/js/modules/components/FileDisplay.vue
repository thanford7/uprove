<template>
    <font-awesome-icon :icon="['far', fileIcon]"/>&nbsp;
    <a v-if="file.file" :href="file.file" download style="overflow-wrap: break-word;">
        <font-awesome-icon :icon="['fas', 'download']"/>&nbsp;
        {{(isUseFileName) ? file.fileName : file.title}}
    </a>
    <span v-else>{{file.title}}</span>&nbsp;<BadgesSkillLevels v-if="isIncludeSkillLevels" :skillLevels="getSkillLevelsFromBits(file.skillLevelBits)"/>
    <p v-if="isIncludeDescription" class="-sub-text">{{file.description}}</p>
</template>

<script>
import BadgesSkillLevels from "./BadgesSkillLevels";
import dataUtil from "../../utils/data";

export default {
    name: "FileDisplay.vue",
    props: ['file', 'isIncludeDescription', 'isIncludeSkillLevels', 'isUseFileName'],
    components: {BadgesSkillLevels},
    computed: {
        fileIcon() {
            const fileType = dataUtil.getFileType(this.file.fileName);
            if (!fileType) {
                return 'file';
            }
            if (fileType.includes('xls') || fileType.includes('csv')) {
                return 'file-excel';
            }
            if (fileType.includes('ppt')) {
                return 'file-powerpoint';
            }
            if (fileType === 'pdf') {
                return 'file-pdf';
            }
            if (fileType.includes('doc')) {
                return 'file-word'
            }
            if (this.globalData.ALLOWED_UPLOADS.IMAGE.includes(fileType)) {
                return 'file-image';
            }
            if (this.globalData.ALLOWED_UPLOADS.VIDEO.includes(fileType)) {
                return 'file-video';
            }
            return 'file';
        }
    },
    methods: {
        getSkillLevelsFromBits(skillLevelBits) {
            return dataUtil.getSkillLevelsFromBits(skillLevelBits, this.globalData.SKILL_LEVEL);
        }
    }
}
</script>