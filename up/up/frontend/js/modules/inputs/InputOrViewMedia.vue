<template>
    <div>
        <label :for="inputId" class="form-label">{{capitalizedItemLabel}}</label>
        <div v-if="!isUpload" class="mb-1">
            <img :src="currentItem" style="height: 40px;"><br>
            <a href="#" @click="toggleUpload(true)">Change {{itemLabel}}</a>
        </div>
        <InputMedia v-if="isUpload" :elId="inputId" :mediaTypes="mediaTypes" @selected="$emit('selectedMediaNew', $event)"/>
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
        }
    },
    components: {InputMedia},
    computed: {
        capitalizedItemLabel() {
            return dataUtil.capitalize(this.itemLabel);
        },
        isNewUpload() {
            return this.currentItem && this.currentItem instanceof File
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