<template>
    <div class="row">
        <div class="col-3 col-md-2 p-0 d-flex align-items-center justify-content-center">
            <img v-if="contentItem.organization.logo" :src="contentItem.organization.logo">
            <i v-else class="fas fa-chalkboard-teacher fa-2x"></i>
        </div>
        <div class="col-9">
            <div>Issued: {{formatDate(contentItem.issueDate)}}</div>
            <div v-if="contentItem.hasExpiration">Expires: {{formatDate(contentItem.expirationDate)}}</div>
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