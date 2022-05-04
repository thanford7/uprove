<template>
    <div>
        <div class="row mb-2">
            <div class="col-3 col-md-2 p-0 d-flex align-items-center justify-content-center">
                <img v-if="contentItem.school.logo" :src="contentItem.school.logo">
                <i v-else class="fas fa-chalkboard-teacher fa-2x"></i>
            </div>
            <div class="col-9">
                {{contentItem.degreeSubject}}<br>
                <template v-if="contentItem.startDate">
                    {{formatDate(contentItem.startDate)}} to {{formatDate(contentItem.endDate) || 'current'}}
                </template>
                <div v-if="hasActivities" class="pt-2">
                    Activities:<br>
                    <div class="-no-child-margin" v-html="truncatedActivities"></div>
                    <a
                        v-if="truncatedActivities.length !== contentItem.activities.length"
                        href="#"
                        @click="eventBus.emit('open:displayContentModal', contentItem)"
                    >See more</a>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import dataUtil from '../../../utils/data';
import form from "../../../utils/form";
import clip from "text-clipper";

export default {
    props: {
        contentItem: {
            type: Object
        }
    },
    computed: {
        hasActivities() {
            return !form.isEmptyWysiwyg(this.contentItem.activities);
        },
        truncatedActivities() {
            return clip(this.contentItem.activities, 200, {html: true});
        }
    },
    methods: {
        formatDate(dateVal) {
            return dataUtil.formatDate(dateVal, {dateFormat: dataUtil.shorthandDateFormat, isReturnNull: true});
        }
    }
}
</script>