<template>
    <div>
        <MediaSelectize 
            ref="existingSel" 
            :currentMediaIds="currentMediaIds"
            :mediaTypes="mediaTypes"
            :isMultiUpload="isMultiUpload"
            :placeholder="`Select existing ${placeholderText}...`"
            @selected="selectedVal = $event" 
        />
        <InputMedia 
            ref="newUpload"
            :mediaTypes="mediaTypes"
            :isMultiUpload="isMultiUpload"
            @selected="uploadVal = $event"
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
            isUpload: false,
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
        currentMediaIds: {
            type: Array
        },
        isMultiUpload: {
            type: Boolean
        },
        placeholderDescription: {
            type: String
        }
    },
    components: {InputMedia, MediaSelectize},
    methods: {
        toggleUpload(isUpload) {
            this.isUpload = isUpload;
            $(this.$refs.newUpload.$el).toggle(isUpload);
            $(this.$refs.existingSel.$el).parent().find('.selectize-control').toggle(!isUpload);
        },
        getValue() {
            return {
                uploadValue: (this.isUpload) ? this.uploadVal : null,
                existingValue: (this.isUpload) ? null : this.selectedVal
            }
        }
    },
    mounted() {
        this.toggleUpload(false);
    }
}
</script>