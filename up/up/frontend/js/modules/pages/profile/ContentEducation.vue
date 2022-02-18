<template>
    <div class="card-body">
        <div class="col-12 p-0"><img :src="contentItem.school.logo" style="max-height: 50px; max-width: 75%;"></div>
        <div><b>{{contentItem.school.name}}</b></div>
        <div class="w-100"></div>
        <div class="-text-medium">
            {{contentItem.degree}}<br>
            {{contentItem.degreeSubject}}<br>
            <template v-if="contentItem.startDate">
                {{formatDate(contentItem.startDate)}} to {{formatDate(contentItem.endDate) || 'current'}}
            </template>
        </div>

        <div v-if="contentItem.activities" class="-sub-text">
            Activities:<br>
            <div v-html="contentItem.activities"></div>
        </div>
    </div>
</template>
<script>
import dataUtil from '../../../utils/data';

export default {
    props: {
        contentItem: {
            type: Object
        }
    },
    methods: {
        formatDate(dateVal) {
            return dataUtil.formatDate(dateVal, {dateFormat: dataUtil.shorthandDateFormat, isReturnNull: true});
        }
    }
}
</script>