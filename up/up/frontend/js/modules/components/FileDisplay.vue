<template>
    <font-awesome-icon :icon="['far', fileIcon]"/>&nbsp;
    <a v-if="file.file" :href="file.file" download style="overflow-wrap: break-word;">
        <font-awesome-icon :icon="['fas', 'download']"/>&nbsp;
        {{(isUseFileName) ? file.fileName : file.title}}
    </a>
    <span v-else>{{file.title}}</span>
    <p v-if="isIncludeDescription">{{file.description}}</p>
</template>

<script>
import data from "../../utils/data";

export default {
    name: "FileDisplay.vue",
    props: ['file', 'isIncludeDescription', 'isUseFileName'],
    computed: {
        fileIcon() {
            const fileType = data.getFileType(this.file.fileName);
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
    }
}
</script>