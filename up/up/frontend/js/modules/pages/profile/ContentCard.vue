<template>
    <div :id="elId" class="card col-md-5 col-12 mb-3">
        <div class="card-inner">
            <h5 class="card-header">
                {{cardTitle}}
                <span v-if="initData.isOwner" class="card-edit-options">
                    <i
                        title="Edit content card"
                        class="fas fa-pencil-alt"
                        @click="eventBus.emit(openEvent, item)"
                    />
                    <i
                        title="Delete content card"
                        class="fas fa-trash"
                        @click="removeCard"
                    />
                    <i
                        v-if="contentItem.contentOrder !== 1"
                        @click="move(-1)"
                        class="fas"
                        :class="`fa-arrow-${(isMobile) ? 'up' : 'left'}`"
                        :title="`Move content card ${(isMobile) ? 'up' : 'left'}`"
                    />
                    <i
                        v-if="contentItem.contentOrder !== contentSection.sectionItems.length"
                        @click="move(1)"
                        class="fas"
                        :class="`fa-arrow-${(isMobile) ? 'down' : 'right'}`"
                        :title="`Move content card ${(isMobile) ? 'down' : 'right'}`"
                    />
                </span>
            </h5>
            <template v-if="item">
                <ContentMedia
                    v-if="item.type === contentTypes.CUSTOM"
                    :contentItem="item"
                    @contentUpdated="adjustCardHeight"
                />
                <ContentCertification v-if="item.type === contentTypes.CERTIFICATION" :contentItem="item"/>
                <ContentEducation v-if="item.type === contentTypes.EDUCATION" :contentItem="item"/>
                <ContentExperience v-if="item.type === contentTypes.EXPERIENCE" :contentItem="item"/>
                <ContentProject v-if="item.type === contentTypes.PROJECT" :contentItem="item"/>
                <ViewMoreLink v-if="isHeightExceeded || item.type === contentTypes.PROJECT" @click="eventBus.emit('open:displayContentModal', item)"/>
            </template>
        </div>
    </div>
</template>
<script>
import {CONTENT_TYPES} from '../../../globalData';
import ContentCertification from "./ContentCertification";
import ContentEducation from './ContentEducation.vue';
import ContentExperience from './ContentExperience.vue';
import ContentMedia from './ContentMedia.vue';
import ContentProject from "./ContentProject";
import contentUtil from "../../../utils/content";
import dataUtil from "../../../utils/data";
import Layout from '../../../utils/layout';
import ViewMoreLink from '../../components/ViewMoreLink.vue';

export default {
    data() {
        return {
            elId: this.getNewElUid(),
            crudUrl: 'user-profile/section/content-item/',
            isUpdateData: true,
            updateDeleteMethod: 'POST',
            el$: null,
            cardInner$: null,
            isHeightExceeded: null,
            contentTypes: CONTENT_TYPES
        }
    },
    components: {
        ContentCertification,
        ContentMedia,
        ContentEducation,
        ContentExperience,
        ContentProject,
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
    watch: {
        contentItem() {
            this.adjustCardHeight();
        }
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
        adjustCardHeight() {
            if (this.cardInner$ && this.el$) {
                this.el$.css('height', `${this.cardInner$.outerHeight(true)}px`); // Hack to get each card to be a different height
                this.cardInner$.css('column-width', this.cardInner$.width());
                this.isHeightExceeded = Layout.isElHeightExceeded(this.el$);
            }
        },
        move(direction) {
            this.formData = {
                id: this.contentItem.id,
                contentOrder: this.contentItem.contentOrder + direction,
                sectionId: this.contentSection.id
            }
            this.saveChange(null, true);
        }
    },
    mounted() {
        if (!this.el$) {
            this.el$ = $(`#${this.elId}`);
            this.cardInner$ = this.el$.find('.card-inner');
            this.adjustCardHeight();
            this.isHeightExceeded = Layout.isElHeightExceeded(this.el$);
        }

        this.eventBus.on('resize', () => { this.adjustCardHeight(); });
    },
}
</script>