<template>
    <div class="row mt-3 mb-2">
        <div class="align-items-center" style="display: flex">
            <img v-if="image" :src="image" class="employer-logo">
            <h3 v-else-if="imageAlt" style="display: inline-block; margin-bottom: 0">{{imageAlt}}&nbsp;|&nbsp;</h3>
            <h3 style="display: inline-block; margin-bottom: 0">{{title}}</h3>
        </div>
    </div>
</template>

<script>
export default {
    name: "PageHeader",
    props: ['title', 'image', 'imageAlt']
}
</script>