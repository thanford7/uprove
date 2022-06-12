<template>
    <div :id="elId" class="col-12 content-item">
        <div class="item-header">
            <h6 class="after-border-middle d-flex align-items-center fw-bolder">
                {{cardTitle}}
            </h6>
            <div>
                <span v-if="initData.isOwner" class="item-edit-options">
                    <i
                        v-if="item.type !== contentTypes.PROJECT"
                        title="Edit content"
                        class="fas fa-pencil-alt"
                        @click="eventBus.emit(openEvent, item)"
                    />
                    <i
                        title="Remove content"
                        class="fas fa-trash"
                        @click="removeCard"
                    />
                </span>
            </div>
        </div>
        <template v-if="item">
            <ContentCertification v-if="item.type === contentTypes.CERTIFICATION" :contentItem="item"/>
            <ContentEducation v-if="item.type === contentTypes.EDUCATION" :contentItem="item"/>
            <ContentExperience v-if="item.type === contentTypes.EXPERIENCE" :contentItem="item"/>
            <ContentProject v-if="item.type === contentTypes.PROJECT" :contentItem="item"/>
        </template>
    </div>
</template>
<script>
import {CONTENT_TYPES} from '../../../globalData';
import ContentCertification from "./ContentCertification";
import ContentEducation from './ContentEducation.vue';
import ContentExperience from './ContentExperience.vue';
import ContentProject from "./ContentProject";
import contentUtil from "../../../utils/content";
import dataUtil from "../../../utils/data";
import EvaluationScoreBadge from "./EvaluationScoreBadge";
import ViewMoreLink from '../../components/ViewMoreLink.vue';

export default {
    data() {
        return {
            elId: this.getNewElUid(),
            crudUrl: 'user-profile/section/content-item/',
            isUpdateData: true,
            updateDeleteMethod: 'POST',
            el$: null,
            contentTypes: CONTENT_TYPES
        }
    },
    components: {
        ContentCertification,
        ContentEducation,
        ContentExperience,
        ContentProject,
        EvaluationScoreBadge,
        ViewMoreLink
    },
    computed: {
        item() {
            return this.contentItem.item;
        },
        cardTitle() {
            return contentUtil.getContentTitle(this.item);
        },
        openEvent() {
            let openType;
            if (this.item.type === this.contentTypes.CUSTOM) {
                openType = 'Media';
            } else if (this.item.type === this.contentTypes.PROJECT) {
                openType = 'UserProject';
            } else {
                openType = dataUtil.capitalize(this.item.type);
            }
            return `open:edit${openType}Modal`
        },
    },
    props: ['contentItem', 'contentSection'],
    methods: {
        getDeleteConfirmationMessage() {
            return `Are you sure you want to remove this ${this.item.type} card? This will not delete it, only remove it from the page.`
        },
        removeCard() {
            this.formData = {
                id: this.contentItem.id
            }
            this.deleteObject();
        },
    },
}
</script>