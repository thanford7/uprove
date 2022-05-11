<template>
    <div class="input-image" :id="elId">
        <div class="d-flex align-items-center">
            <InfoToolTip :content="`Supported file types are ${supportedFormatsString}`" :elId="getNewElUid()"/>&nbsp;
            <input
                ref="fileInput"
                type="file"
                class="form-control"
                :accept="acceptFormatsString"
                :multiple="isMultiUpload"
                @change="$emit('selected', getFileData())"
                style="display: inline-block; flex-grow: 1"
            >
        </div>
    </div>
</template>
<script>
import InfoToolTip from "../components/InfoToolTip";

export default {
    components: {InfoToolTip},
    data() {
        return {
            supportedFormats: {
                image: ['png', 'jpeg', 'jpg', 'gif'],
                video: ['mp4', 'm4v', 'mov', 'wmv', 'avi', 'mpg', 'webm'],
                file: ['doc', 'docx', 'pdf', 'xls', 'xlsx', 'ppt', 'pptx', 'twb', 'twbx', 'pages', 'numbers', 'key', 'gdoc', 'gslides', 'gsheet', 'py']
            }
        }
    },
    computed: {
        allowedFormats() {
            return this.supportedFormatsOverride || this.mediaTypes.reduce((allFormats, mediaType) => {
                allFormats = [...allFormats, this.supportedFormats[mediaType]];
                return allFormats;
            }, [])
        },
        acceptFormatsString() {
            return this.allowedFormats.map((fileFormat) => `.${fileFormat}`).join(',');
        },
        supportedFormatsString() {
            return this.allowedFormats.join(', ');
        }
    },
    props: {
        mediaTypes: {
            type: Array,
            required: true
        },
        isMultiUpload: Boolean,
        elId: String,
        value: String,
        supportedFormatsOverride: [Array, null]
    },
    methods: {
        clear() {
            this.$refs.fileInput.value = '';
        },
        getFileData() {
            const files = this.$refs.fileInput.files;
            // Need to destructure files because it is of type "FileList" which doesn't offer array methods
            return (this.isMultiUpload) ? [...files] : files[0];
        }

    }
}
</script>