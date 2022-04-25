<template>
    <div :id="elId" class="col-12 mb-2 content-item">
        <div class="item-header">
            <h6>
                {{cardTitle}}
            </h6>
            <div>
                <span v-if="initData.isOwner" class="item-edit-options">
                    <i
                        title="Edit content"
                        class="fas fa-pencil-alt"
                        @click="eventBus.emit(openEvent, item)"
                    />
                    <i
                        title="Remove content"
                        class="fas fa-trash"
                        @click="removeCard"
                    />
                    <template v-if="item.type !== contentTypes.PROJECT">
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
                    </template>
                </span>
            </div>
        </div>
        <template v-if="item">
            <ContentCertification v-if="item.type === contentTypes.CERTIFICATION" :contentItem="item"/>
            <ContentEducation v-if="item.type === contentTypes.EDUCATION" :contentItem="item"/>
            <ContentExperience v-if="item.type === contentTypes.EXPERIENCE" :contentItem="item"/>
            <ContentProject v-if="item.type === contentTypes.PROJECT" :contentItem="item"/>
            <ViewMoreLink v-if="isHeightExceeded || item.type === contentTypes.PROJECT" @click="eventBus.emit('open:displayContentModal', item)"/>
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