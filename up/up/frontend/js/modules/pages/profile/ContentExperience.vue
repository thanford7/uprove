<template>
    <div class="card-body">
        <div class="row" v-if="contentItem">
            <div class="col-12 p-0"><img :src="contentItem.organization.logo" style="max-height: 50px; max-width: 75%;"></div>
            <div class="w-100"></div>
            <div class="-text-medium">
                {{contentItem.positionTitle}}<br>
                {{contentItem.employmentType}}<br>
                {{formatDate(contentItem.startDate)}} to {{formatDate(contentItem.endDate) || 'current'}}
            </div>
            <div v-if="hasDescription" class="card-body pt-1 pb-1">
                <div v-if="hasDescription" v-html="contentItem.description" class="-sub-text"></div>
            </div>
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