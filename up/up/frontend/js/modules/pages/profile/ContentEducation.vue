<template>
    <div class="card-body">
        <template v-for="(educationItem, idx) in educationContentItems" :key="educationItem.ID">
            <div class="row" :class="(idx === 0) ? 'pb-1' : '-border-top--light pt-1'">
                <div class="col-4"><img :src="educationItem.guid" alt="School logo"></div>
                <div class="col-8"><b>{{educationItem.school_name}}</b></div>
                <div class="w-100"></div>
                <div class="-text-medium">
                    {{educationItem.degree_type}}<br>
                    {{educationItem.degree_subject}}<br>
                    {{formatDate(educationItem.start_date)}} to {{formatDate(educationItem.end_date) || 'current'}}
                </div>

                <div v-if="educationItem.activities" class="-sub-text">
                    Activities:<br>
                    {{educationItem.activities}}
                </div>
            </div>
        </template>
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
        educationContentItems() {
            // Filter out any unsaved education content items (these will have the prefix "new")
            return this.contentItem.contentItems.filter((educationContentItem) => !educationContentItem.ID.includes('new'));
        }
    },
    methods: {
        formatDate(dateVal) {
            return dataUtil.formatDate(dateVal, {dateFormat: this.dateFormat, isReturnNull: true});
        }
    }
}
</script>