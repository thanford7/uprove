<template>
    <div class="card col-md-3 mb-3" v-if="cardItem" :id="elId">
        <slot name="topImage"></slot>
        <div class="card-inner">
            <div class="card-header">
                <slot name="header"></slot>
            </div>
            <div class="card-body">
                <slot name="body"></slot>
                <ViewMoreLink v-if="isHeightExceeded && isShowViewMoreLink" :clickFn="getMoreContentFn" :elId="getNewElUid()"/>
            </div>
        </div>
    </div>
</template>
<script>
import Layout from '../../utils/layout';
import ViewMoreLink from "./ViewMoreLink";

export default {
    data() {
        return {
            el$: null,
            cardInner$: null,
            isHeightExceeded: null
        }
    },
    components: {
        ViewMoreLink
    },
    props: {
        cardItem: {
            type: Object
        },
        cardModalName: {
            type: String
        },
        elId: {
            type: String
        },
        isShowViewMoreLink: {
            type: Boolean,
            default: true
        }
    },
    methods: {
        getMoreContentFn() {
            this.eventBus.emit(`open:${this.cardModalName}`, this.cardItem);
        }
    },
    mounted() {
        if (!this.el$) {
            this.el$ = $(`#${this.elId}`);
            this.cardInner$ = this.el$.find('.card-inner');
            this.isHeightExceeded = Layout.isElHeightExceeded(this.el$);
        }
    }
}
</script>