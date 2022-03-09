<template>
    <div v-if="contentItem">
        <template v-for="(section, idx) in contentItem.sections">
            <template v-if="idx === 0">
                <template v-if="section.item">
                    <video v-if="section.item.type === contentTypes.VIDEO" controls :src="section.item.video" @resize="$emit('contentUpdated')"></video>
                    <img v-if="section.item.type === contentTypes.IMAGE" :src="section.item.image" alt="Banner media" class="card-img-top">
                </template>
            </template>
            <div v-else class="card-body pt-1 pb-1">
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
    </div>
</template>
<script>
import {CONTENT_TYPES} from '../../../globalData';
import FileDisplay from "../../components/FileDisplay";
import form from "../../../utils/form";

export default {
    data() {
        return {
            contentTypes: CONTENT_TYPES
        }
    },
    components: {FileDisplay},
    props: {
        contentItem: Object
    },
    methods: {
        hasText(text) {
            return !form.isEmptyWysiwyg(text);
        }
    }
}
</script>