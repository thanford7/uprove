<template>
    <div class="card-body">
        <div class="row">
            <div class="col-3 p-0">
                <img v-if="contentItem.organization.logo" :src="contentItem.organization.logo">
                <i v-else class="fas fa-chalkboard-teacher fa-2x"></i>
            </div>
            <div class="col-9">
                <div><b>{{contentItem.organization.name}}</b></div>
                <div class="-text-medium">
                    <div>{{contentItem.title}}</div>
                    <div>Issued: {{formatDate(contentItem.issueDate)}}</div>
                    <div v-if="contentItem.hasExpiration">Expires: {{formatDate(contentItem.expirationDate)}}</div>
                </div>
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