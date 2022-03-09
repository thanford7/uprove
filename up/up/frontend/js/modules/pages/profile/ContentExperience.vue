<template>
    <div class="card-body">
        <div class="row mb-2">
            <div class="col-3 p-0">
                <img v-if="contentItem.organization.logo" :src="contentItem.organization.logo">
                <i v-else class="fas fa-building fa-2x"></i>
            </div>
            <div class="col-9">
                {{contentItem.positionTitle}}<br>
                {{contentItem.employmentType}}<br>
                {{formatDate(contentItem.startDate)}} to {{formatDate(contentItem.endDate) || 'current'}}
            </div>
        </div>
        <div v-if="hasDescription" class="row -border-top--light">
            <div class="col-12 pt-2" v-html="contentItem.description"></div>
        </div>
    </div>
</template>
<script>
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
        }
    },
    methods: {
        formatDate(dateVal) {
            return dataUtil.formatDate(dateVal, {dateFormat: dataUtil.shorthandDateFormat, isReturnNull: true});
        }
    }
}
</script>