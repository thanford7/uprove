<template>
    <div>
        <MediaSelectize 
            ref="existingSel"
            :currentVal="currentVal"
            :mediaTypes="mediaTypes"
            :assetsKey="assetsKey"
            :isMultiUpload="isMultiUpload"
            :placeholder="`Select existing ${placeholderText}...`"
            @selectedMedia="$emit('selectedMediaExisting', $event)"
        />
        <InputMedia
            ref="newUpload"
            :mediaTypes="mediaTypes"
            :isMultiUpload="isMultiUpload"
            @selected="$emit('selectedMediaNew', $event)"
        />
        <a href="#" ref="toggleUpload" @click="toggleUpload(!isUpload)">{{selectPlaceholderText}}</a>
    </div>
</template>
<script>
import InputMedia from './InputMedia.vue';
import MediaSelectize from './MediaSelectize.vue';

export default {
    data() {
        return {
            uploadVal: null,
            isUpload: true,
            selectedVal: null,
        }
    },
    computed: {
        placeholderText() {
            return this.placeholderDescription || this.mediaTypes.join(' or ')
        },
        selectPlaceholderText() {
            return (this.isUpload) ? `Select existing ${this.placeholderText}` : `Upload new ${this.placeholderText}`;
        }
    },
    props: {
        mediaTypes: {
            type: Array,
            required: true
        },
        isMultiUpload: Boolean,
        placeholderDescription: String,
        currentVal: [String, Number],
        assetsKey: {
            type: String,
            default: 'assets'
        }
    },
    components: {InputMedia, MediaSelectize},
    methods: {
        toggleUpload(isUpload) {
            this.isUpload = isUpload;
            $(this.$refs.newUpload.$el).toggle(isUpload);
            $(this.$refs.existingSel.$el).parent().find('.selectize-control').toggle(!isUpload);
        }
    },
    mounted() {
        this.toggleUpload(this.isUpload);
    }
}
</script>