<template>
    <div class="card-body">
        <div class="row" v-if="contentItem">
            <div class="col-4"><img :src="(contentItem.logo) ? contentItem.logo.guid : ''" alt="Company logo"></div>
            <div class="col-8"><b>{{contentItem.company}}</b></div>
            <div class="w-100"></div>
            <div class="-text-medium">
                {{contentItem.position_title}}<br>
                {{contentItem.employment_type}}<br>
                {{formatDate(contentItem.start_date)}} to {{formatDate(contentItem.end_date) || 'current'}}
            </div>
            <div v-if="hasDescription" class="card-body pt-1 pb-1">
                <div v-if="hasDescription" v-html="contentItem.description" class="-sub-text"></div>
            </div>
        </div>
    </div>
</template>
<script>
import dataUtil from '../../../utils/data';


export default {
    data() {
        return {
            dateFormat: 'MMM YYYY'
        }
    },
    props: {
        contentItem: {
            type: Object
        }
    },
    computed: {
        // Tiptap adds a p element as the template. If the description is just that, there is no content.
        hasDescription() {
            return Boolean(this.contentItem.description) && this.contentItem.description !== '<p></p>';
        }
    },
    methods: {
        formatDate(dateVal) {
            return dataUtil.formatDate(dateVal, {dateFormat: this.dateFormat, isReturnNull: true});
        }
    }
}
</script>