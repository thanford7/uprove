<template>
    <div class="view-more" :id="_uid">
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
        }
    },
    mounted() {
        if(!this.el$) {
            this.el$ = $(`#${this._uid}`);
            if (this.clickFn) {
                this.el$.find('a').on('click', this.clickFn);
            }
        }
    }
}
</script>