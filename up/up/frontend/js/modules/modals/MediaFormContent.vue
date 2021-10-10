<template>
    <div>
        <div class="mb-3">
            <label for="formContentTitle" class="form-label">Title</label>
            <input type="text" class="form-control" placeholder="Add title..." id="formContentTitle" v-model="formData.title">
        </div>
        <div class="mb-3">
            <label class="form-label">Banner {{allowedBannerMediaTypes.join(' or ')}}</label>
            <InputSelectOrUploadMedia
                ref="mediaInput"
                :mediaTypes="allowedBannerMediaTypes"
                :currentMediaIds="[contentItem.mediaId]"
                :isMultiUpload="false"
            />
        </div>
        <div class="mb-3">
            <label class="form-label">Description</label>
            <InputWsiwyg placeholder="Add a description..." v-model="formData.description"/>
        </div>
        <div v-if="contentType === 'project'" class="mb-3">
            <label class="form-label">Files</label>
            <InputSelectOrUploadMedia
                ref="fileInput"
                :mediaTypes="['file']"
                :currentMediaIds="(contentItem.files || []).map((file) => file.id)"
                :isMultiUpload="true"
            />
        </div>
    </div>
</template>
<script>
import {mapState} from 'vuex';
import InputSelectOrUploadMedia from '../inputs/InputSelectOrUploadMedia.vue';
import InputWsiwyg from '../inputs/InputWsiwyg.vue';

export default {
    data() {
        return {
            inputs: {
                title: {
                    setter: () => this.contentItem.post_title
                },
                description: {
                    setter: () => this.contentItem.description
                }
            },
        }
    },
    computed: {
        ...mapState({
            eventBus: 'eventBus'
        })
    },
    props: {
        contentItem: {
            type: Object,
            default: () => ({})
        },
        contentType: {
            type: String
        },
        allowedBannerMediaTypes: {
            type: Array,
            default: () => ['video']
        }
    },
    components: {InputSelectOrUploadMedia, InputWsiwyg},
    computed: {
        formData() {
            const formData = {}
            Object.entries(this.inputs).forEach(([input, cfg]) => {
                formData[input] = cfg.setter();
            });
            return formData;
        }
    },
    methods: {
        async getPreSaveChange() {
            // For some reason, mapState doesn't work within the promise function so we need to grab this function directly
            const createMediaItem = this.$store.state.eventBus.createMediaItem;
            const {uploadValue: uploadMediaValue, existingValue: existingMediaValue} = this.$refs.mediaInput.getValue();
            const data = {...this.formData};
            if (uploadMediaValue) {
                data.media = await createMediaItem(uploadMediaValue);
            } else {
                data.media = existingMediaValue;
            }
            if (this.contentType === 'project') {
                const {uploadValue: uploadFilesValue, existingValue: existingFilesValue} = this.$refs.fileInput.getValue();
                if (uploadFilesValue) {
                    const filePromises = [];
                    filesVal.forEach((file) => {
                        filePromises.push(createMediaItem(file));
                    });
                    data.files = await Promise.allSettled(filePromises).then((results) => results.map((result) => result.value));
                }
                if (existingFilesValue) {
                    data.files = [...(data.files || []), ...existingFilesValue];
                }
            }
            return data;
        }
    }
}
</script>