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
}
</script>