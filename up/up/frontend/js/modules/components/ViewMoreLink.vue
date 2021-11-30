<template>
    <div class="view-more" :id="elId">
        <a :href="href">{{text}}</a>
    </div>
</template>
<script>
export default {
    data() {
        return {
            el$: null
        };
    },
    props: {
        href: {
            type: String,
            default: '#'
        },
        text: {
            type: String,
            default: 'View more...'
        },
        clickFn: {
            type: Function
        },
        elId: {
            type: String,
        }
    },
    mounted() {
        if(!this.el$) {
            this.el$ = $(`#${this.elId}`);
            if (this.clickFn) {
                this.el$.find('a').on('click', this.clickFn);
            }
        }
    }
}
</script>