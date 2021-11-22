<template>
    <div class="input-image" :id="elId">
        <input 
            ref="fileInput"
            type="file"
            class="form-control"
            :accept="acceptFormatsString"
            :multiple="isMultiUpload"
            @change="$emit('selected', getFileData())"
        >
        <span class="-sub-text">Supported file types are {{supportedFormatsString}}</span>
    </div>
</template>
<script>
export default {
    data() {
        return {
            supportedFormats: {
                image: ['png', 'jpeg', 'jpg', 'gif'],
                video: ['mp4', 'm4v', 'mov', 'wmv', 'avi', 'mpg'],
                file: ['doc', 'docx', 'pdf', 'xls', 'xlsx', 'ppt', 'pptx', 'twb', 'twbx', 'pages', 'numbers', 'key', 'gdoc', 'gslides', 'gsheet']
            }
        }
    },
    computed: {
        acceptFormatsString() {
            return this.mediaTypes.map((mediaType) => {
                return this.supportedFormats[mediaType].map((fileFormat) => `.${fileFormat}`).join(',');
            }).join(',');
        },
        supportedFormatsString() {
            return this.mediaTypes.map((mediaType) => {
                return this.supportedFormats[mediaType].join(', ');
            }).join(', ');
        }
    },
    props: {
        mediaTypes: {
            type: Array,
            required: true
        },
        isMultiUpload: {
            type: Boolean
        },
        elId: {
            type: String
        }
    },
    methods: {
        getFileData() {
            const files = this.$refs.fileInput.files;
            // Need to destructure files because it is of type "FileList" which doesn't offer array methods
            return (this.isMultiUpload) ? [...files] : files[0];
        }
    }
}
</script>