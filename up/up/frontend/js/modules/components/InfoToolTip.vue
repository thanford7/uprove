<template>
    <span :id="elId">
        <font-awesome-icon :icon="['fas', 'info-circle']"/>
        <slot></slot>
    </span>
</template>

<script>
import {Popover} from "bootstrap";

export default {
    name: "InfoToolTip",
    props: ['content', 'elId'],
    mounted() {
        const el$ = $(`#${this.elId}`);
        let container = 'body';
        const modalParent = el$.parents('.modal');
        if (modalParent.length) {
            container = `#${$(modalParent[0]).attr('id')}`;
        }
        new Popover(el$, {
            content: this.content,
            container,
            placement: 'auto',
            trigger: 'hover'
        });
    }
}
</script>