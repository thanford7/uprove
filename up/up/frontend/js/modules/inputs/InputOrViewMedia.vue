<template>
    <div>
        <label :for="inputId" class="form-label">{{capitalizedItemLabel}}</label>
        <div v-if="!isUpload" class="mb-1">
            <div>
                <img v-if="isImage" :src="currentItem" style="height: 40px;" :alt="getFileNameFromUrl(currentItem)">
                <span v-else>{{ getFileNameFromUrl(currentItem) }}</span>
            </div>
            <a href="#" @click="toggleUpload(true)">Change {{itemLabel}}</a>
        </div>
        <InputMedia
            v-if="isUpload"
            :elId="inputId"
            :mediaTypes="mediaTypes"
            :supportedFormatsOverride="supportedFormatsOverride"
            @selected="$emit('selectedMediaNew', $event)"
        />
        <a v-if="!isUploadDefault && !isNewUpload && isUpload" href="#" @click="toggleUpload(false)">Use existing {{itemLabel}}</a>
    </div>
</template>

<script>
import dataUtil from "../../utils/data";
import InputMedia from "./InputMedia";

export default {
    name: "InputOrViewMedia.vue",
    props: {
        inputId: String,
        mediaTypes: Array,
        itemLabel: String,
        currentItem: [String, Object],
        isUploadDefault: {
            type: Boolean,
            default: false
        },
        supportedFormatsOverride: [Array, null]
    },
    components: {InputMedia},
    computed: {
        capitalizedItemLabel() {
            return dataUtil.capitalize(this.itemLabel, false);
        },
        isNewUpload() {
            return this.currentItem && this.currentItem instanceof File
        },
        isImage() {
            return this.globalData.ALLOWED_UPLOADS.IMAGE.includes(dataUtil.getFileType(this.currentItem));
        }
    },
    watch: {
        currentItem(val) {
            this.isUpload = Boolean(!val) || this.isNewUpload;
        }
    },
    data() {
        return {
            isUpload: true
        }
    },
    methods: {
        getFileNameFromUrl: dataUtil.getFileNameFromUrl.bind(dataUtil),
        toggleUpload(isShown) {
            this.isUpload = isShown;
            $(`#${this.inputId}`).toggle(isShown);
        }
    },
    mounted() {
        this.isUpload = this.isUploadDefault;
    }
}
</script>