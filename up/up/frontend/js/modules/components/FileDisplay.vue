<template>
    <span class="-no-wrap">
        <i class="far" :class="`fa-${fileIcon}`"></i>&nbsp;
        <span>{{(isUseFileName || !file.title) ? file.fileName : file.title}}&nbsp;</span>
        <a v-if="fileUrl && !isPreventDownload" :href="fileUrl" download style="overflow-wrap: break-word;" :target="(fileType === FILE_TYPES.PDF) ? '_blank' : ''">
            <i class="fas fa-download"></i>
        </a>&nbsp;
        <span v-if="!fileUrl">{{file.title}}</span>
    </span>
    <p v-if="isIncludeDescription" class="-sub-text">{{file.description}}</p>
</template>

<script>
import dataUtil from "../../utils/data";

const FILE_TYPES = {
    FILE: 'file',
    EXCEL: 'excel',
    POWERPOINT: 'powerpoint',
    PDF: 'pdf',
    WORD: 'word',
    IMAGE: 'image',
    VIDEO: 'video'
};

export default {
    name: "FileDisplay.vue",
    props: ['file', 'isIncludeDescription', 'isIncludeSkillLevels', 'isUseFileName', 'isPreventDownload'],
    data() {
        return {
            FILE_TYPES
        }
    },
    computed: {
        fileUrl() {
            return this.file.file || this.file.image || this.file.video;
        },
        fileType() {
            const fileExtension = dataUtil.getFileType(this.fileUrl);
            if (!fileExtension) {
                return FILE_TYPES.FILE;
            }
            if (fileExtension.includes('xls') || fileExtension.includes('csv')) {
                return FILE_TYPES.EXCEL;
            }
            if (fileExtension.includes('ppt')) {
                return FILE_TYPES.POWERPOINT;
            }
            if (fileExtension === 'pdf') {
                return FILE_TYPES.PDF;
            }
            if (fileExtension.includes('doc')) {
                return FILE_TYPES.WORD;
            }
            if (this.globalData.ALLOWED_UPLOADS.IMAGE.includes(fileExtension)) {
                return FILE_TYPES.IMAGE;
            }
            if (this.globalData.ALLOWED_UPLOADS.VIDEO.includes(fileExtension)) {
                return FILE_TYPES.VIDEO;
            }
            return FILE_TYPES.FILE;
        },
        fileIcon() {
            return (this.fileType === FILE_TYPES.FILE) ? FILE_TYPES.FILE : `file-${this.fileType}`;
        },
    },
}
</script>