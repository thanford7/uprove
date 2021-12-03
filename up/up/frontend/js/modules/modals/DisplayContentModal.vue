<template>
    <BaseModal
        :modalId="modalName"
        :isReadOnly="true"
        :modalTitle="contentItem.post_title"
        :isFooterHidden="true"
        :isScrollable="true"
    >
        <template v-if="['video', 'project'].includes(contentItem.post_type)">
            <div class="row mb-3">
                <video v-if="contentItem.mediaType === 'video'" controls :src="contentItem.mediaGuid"></video>
                <img v-if="contentItem.mediaType === 'image'" :src="contentItem.mediaGuid" alt="Banner media">
            </div>
            <div class="row mb-3">
                <div v-html="contentItem.description"></div>
                <div v-for="file in contentItem.files" :key="file.guid">
                    <font-awesome-icon :icon="['fas', 'external-link-alt']"/> <a :href="file.guid" target="_blank">{{file.title}}</a>
                </div>
            </div>
        </template>
        <template v-if="contentItem.post_type === 'education'">
            <div v-for="educationItem in contentItem.contentItems" :key="educationItem.ID">
                <div class="row mb-3">
                    <div class="col-2"><img :src="educationItem.guid" alt="School logo"></div>
                    <div class="col-10"><b>{{educationItem.school_name}}</b></div>
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
            </div>
        </template>
    </BaseModal>
</template>
<script>
import Modal from 'bootstrap/js/dist/modal';
import {mapGetters, mapState} from 'vuex';
import BaseModal from './BaseModal.vue';
import dataUtil from '../../utils/data';

export default {
    extends: BaseModal,
    components: {BaseModal},
    data() {
        return {
            modalName: 'displayContentModal',
            contentItem: {}
        }
    },
    inheritAttrs: false,
    computed: {
        ...mapGetters({
            getContentItem: 'getContentItem'
        })
    },
    props: {
        id: {
            type: Number
        },
        contentSection: {
            type: String
        }
    },
    methods: {
        hookEvents() {
            this.eventBus.$on('open:displayContentModal', (contentId) => {
                this.contentItem = this.getContentItem(contentId);
                this.modal$.show();
            });
        },
        formatDate(dateVal) {
            return dataUtil.formatDate(dateVal, {dateFormat: this.dateFormat, isReturnNull: true});
        }
    },
}
</script>