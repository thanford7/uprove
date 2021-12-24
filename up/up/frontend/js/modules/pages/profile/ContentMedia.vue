<template>
    <div v-if="contentItem">
        <video v-if="contentItem.mediaType === 'video'" controls :src="contentItem.mediaGuid" @resize="$emit('contentUpdated')"></video>
        <img v-if="contentItem.mediaType === 'image'" :src="contentItem.mediaGuid" alt="Banner media" class="card-img-top">
        <div v-if="hasDescription || (contentItem.files && contentItem.files.length)" class="card-body pt-1 pb-1">
            <div v-if="hasDescription" v-html="contentItem.description"></div>
            <div v-for="file in contentItem.files" :key="file.guid">
                <i class="fas fa-external-link-alt"></i> <a :href="file.guid" target="_blank">{{file.title}}</a>
            </div>
        </div>
    </div>
</template>
<script>

export default {
    props: {
        contentItem: {
            type: Object
        }
    },
    computed: {
        // Tiptap adds a p element as the template. If the description is just that, there is no content.
        hasDescription() {
            return Boolean(this.contentItem.description) && this.contentItem.description !== '<p></p>';
        }
    }
}
</script>