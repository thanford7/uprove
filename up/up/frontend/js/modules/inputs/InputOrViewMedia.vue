<template>
    <div>
        <label :for="inputId" class="form-label">{{capitalizedItemLabel}}</label>
        <div v-if="!isUpload" class="mb-1">
            <img :src="currentItem" style="height: 40px;"><br>
            <a href="#" @click="toggleUpload(true)">Change {{itemLabel}}</a>
        </div>
        <InputMedia v-if="isUpload" :elId="inputId" :mediaTypes="mediaTypes" @selected="$emit('selected', $event)"/>
        <a v-if="!isNewUpload && isUpload" href="#" @click="toggleUpload(false)">Use existing {{itemLabel}}</a>
    </div>
</template>

<script>
import dataUtil from "../../utils/data";
import InputMedia from "./InputMedia";

export default {
    name: "InputOrViewMedia.vue",
    props: ['inputId', 'mediaTypes', 'itemLabel', 'currentItem'],
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
    }
}
</script>