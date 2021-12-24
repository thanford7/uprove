<template>
    <div class="card col-md-3 col-12 mb-3" v-if="contentItem" :id="_uid" :data-content-id="contentId">
        <div class="card-inner">
            <h5 class="card-header">
                {{contentItem.post_title}}
                <span v-if="$store.state.isOwner" class="float-end">
                    <i
                        title="Edit content card"
                        class="fas fa-pencil-alt"
                        @click="eventBus.$emit(openEvent, contentId)"
                        :data-content-item="contentItem"
                    />
                    <i
                        title="Delete content card"
                        class="fas fa-trash"
                        @click="removeCard"
                        :data-content-item="contentItem"
                    />
                    <i
                        title="Delete content card"
                        class="fas fa-trash"
                        @click="removeCard"
                        :data-content-item="contentItem"
                    />
                    <i
                        v-if="!isFirstItem"
                        @click="move(-1)"
                        class="fas"
                        :class="`fa-arrow-${(isMobile) ? 'up' : 'left'}`"
                        :title="`Move content card ${(isMobile) ? 'up' : 'left'}`"
                    />
                    <i
                        v-if="!isLastItem"
                        @click="move(1)"
                        class="fas"
                        :class="`fa-arrow-${(isMobile) ? 'down' : 'right'}`"
                        :title="`Move content card ${(isMobile) ? 'down' : 'right'}`"
                    />
                </span>
            </h5>
            <ContentMedia 
                v-if="['video', 'project'].includes(contentItem.post_type)" 
                :contentItem="contentItem"
                @contentUpdated="adjustCardHeight"
            />
            <ContentEducation v-if="contentItem.post_type === 'education'" :contentItem="contentItem"/>
            <ContentExperience v-if="contentItem.post_type === 'experience'" :contentItem="contentItem"/>
            <ViewMoreLink v-if="isHeightExceeded" :clickFn="getMoreContentFn()"/>
        </div>
    </div>
</template>
<script>
import {mapGetters, mapState} from 'vuex';
import ContentEducation from './ContentEducation.vue';
import ContentExperience from './ContentExperience.vue';
import ContentMedia from './ContentMedia.vue';
import Layout from '../../../utils/layout';
import ViewMoreLink from '../../components/ViewMoreLink.vue';

export default {
    data() {
        return {
            el$: null,
            cardInner$: null,
            isHeightExceeded: null
        }
    },
    components: {
        ContentMedia,
        ContentEducation,
        ContentExperience,
        ViewMoreLink
    },
    computed: {
        contentItem() {
            return {...this.getContentItem(this.contentId)};
        },
        openEvent() {
            let openType;
            if (['video', 'project'].includes(this.contentItem.post_type)) {
                openType = 'Media'
            } else {
                openType = _.capitalize(this.contentItem.post_type)
            }
            return `open:edit${openType}Modal`
        },
        ...mapGetters({
            getContentItem: 'getContentItem'
        })
    },
    watch: {
        contentItem() {
            this.adjustCardHeight();
        }
    },
    props: {
        contentId: {
            type: String
        },
        contentSection: {
            type: String
        },
        contentSectionOrder: {
            type: Number
        },
        contentItemOrder: {
            type: Number
        },
        isFirstItem: {
            type: Boolean
        },
        isLastItem: {
            type: Boolean
        }
    },
    methods: {
        removeCard() {
            if(!window.confirm(`Are you sure you want to remove this ${this.contentSection} card? This will not delete it, only remove it from the page.`)) {
                return;
            }
            this.$store.commit(`remove${_.capitalize(this.contentSection)}Id`, {id: this.contentId, sectionIdx: this.contentSectionOrder});
        },
        getMoreContentFn() {
            return () => this.eventBus.$emit('open:displayContentModal', this.contentItem.ID);
        },
        adjustCardHeight() {
            if (this.cardInner$ && this.el$) {
                this.el$.css('height', `${this.cardInner$.outerHeight(true)}px`); // Hack to get each card to be a different height
                this.cardInner$.css('column-width', this.cardInner$.width());
                this.isHeightExceeded = Layout.isElHeightExceeded(this.el$);
            }
        },
        move(direction) {
            this.$store.commit(`move${_.capitalize(this.contentSection)}Id`, {itemIdx: this.contentItemOrder, sectionIdx: this.contentSectionOrder, direction})
        }
    },
    mounted() {
        if (!this.el$) {
            this.el$ = $(`#${this._uid}`);
            this.cardInner$ = this.el$.find('.card-inner');
            this.adjustCardHeight();
            this.isHeightExceeded = Layout.isElHeightExceeded(this.el$);
        }

        this.eventBus.$on('resize', () => { this.adjustCardHeight(); });
    },
}
</script>