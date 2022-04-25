<template>
    <div>
        <div class="row mb-2">
            <div class="col-3 p-0">
                <img v-if="contentItem.school.logo" :src="contentItem.school.logo">
                <i v-else class="fas fa-chalkboard-teacher fa-2x"></i>
            </div>
            <div class="col-9">
                <div><b>{{contentItem.school.name}}</b></div>
                <div class="-text-medium">
                    {{contentItem.degree}}<br>
                    {{contentItem.degreeSubject}}<br>
                    <template v-if="contentItem.startDate">
                        {{formatDate(contentItem.startDate)}} to {{formatDate(contentItem.endDate) || 'current'}}
                    </template>
                </div>
            </div>
        </div>
        <div v-if="contentItem.activities" class="row -border-top--light">
            <div class="col-12 pt-2">
                Activities:<br>
                <div v-html="contentItem.activities"></div>
            </div>
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