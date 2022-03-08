<template>
    <span :id="elId">
        <i v-if="!isExcludeInfoCircle" class="fas fa-info-circle"></i>
        <slot></slot>
    </span>
</template>

<script>
import {Popover} from "bootstrap";

export default {
    name: "InfoToolTip",
    data() {
        return {
            popover: null
        }
    },
    props: ['content', 'isHtmlContent', 'elId', 'isExcludeInfoCircle'],
    methods: {
        initTooltip() {
            const el$ = $(`#${this.elId}`);
            if (!this.popover && el$.length) {
                let container = 'body';
                const modalParent = el$.parents('.modal');
                if (modalParent.length) {
                    container = `#${$(modalParent[0]).attr('id')}`;
                }
                this.popover = new Popover(el$, {
                    content: this.content,
                    html: this.isHtmlContent || false,
                    container,
                    placement: 'auto',
                    trigger: 'hover'
                });
            }
        }
    },
    mounted() {
        this.initTooltip();
    },
    updated() {
        this.initTooltip();
    }
}
</script>