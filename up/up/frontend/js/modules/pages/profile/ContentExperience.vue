<template>
    <div>
        <div class="row mb-2">
            <div class="col-3 col-md-2 p-0 d-flex align-items-center justify-content-center">
                <img v-if="contentItem.organization.logo" :src="contentItem.organization.logo">
                <i v-else class="fas fa-building fa-2x"></i>
            </div>
            <div class="col-9 d-flex align-items-center">
                <div>
                    {{contentItem.employmentType}}<br>
                    {{formatDate(contentItem.startDate)}} to {{formatDate(contentItem.endDate) || 'current'}}
                </div>
            </div>
        </div>
        <div v-if="hasDescription">
            <div class="col-12 pt-2 -no-child-margin" v-html="truncatedDescription"></div>
            <a
                v-if="truncatedDescription.length !== contentItem.description.length"
                href="#"
                @click="eventBus.emit('open:displayContentModal', contentItem)"
            >See more</a>
        </div>
    </div>
</template>
<script>
import clip from "text-clipper";
import dataUtil from '../../../utils/data';
import form from "../../../utils/form";


export default {
    props: {
        contentItem: {
            type: Object
        }
    },
    computed: {
        hasDescription() {
            return !form.isEmptyWysiwyg(this.contentItem.description);
        },
        truncatedDescription() {
            return clip(this.contentItem.description, 200, {html: true});
        }
    },
    methods: {
        formatDate(dateVal) {
            return dataUtil.formatDate(dateVal, {dateFormat: dataUtil.shorthandDateFormat, isReturnNull: true});
        }
    }
}
</script>