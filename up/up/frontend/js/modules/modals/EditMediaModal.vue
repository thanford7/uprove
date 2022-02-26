<template>
    <BaseModal
        v-if="formData.sections"
        :modalId="modalName"
        :modalTitle="`Edit ${contentType} content`"
        :isLargeDisplay="true"
        :isContentOnly="isContentOnly"
        @saveChange="saveChange"
    >
        <div class="mb-3">
            <label class="form-label">Title</label>
            <input ref="title" type="text" class="form-control" placeholder="Add title..." v-model="formData.title">
        </div>
        <div class="mb-3">
            <label class="form-label">
                Banner {{allowedBannerMediaTypes.join(' or ')}}
                <InfoToolTip :elId="getNewElUid()" content="This will be prominently displayed at the top of the card."/>
            </label>
            <InputSelectOrUploadMedia
                ref="mediaInput"
                :currentVal="getMediaId(formData.sections[0])"
                :mediaTypes="allowedBannerMediaTypes"
                :isMultiUpload="false"
                @selectedMediaNew="setSectionVal($event, 0, true)"
                @selectedMediaExisting="setSectionVal($event, 0, false)"
            />
        </div>
        <div class="mb-3">
            <label class="form-label">Description</label>
            <InputWsiwyg ref="description" placeholder="Add a description..." v-model="formData.sections[1].value"/>
        </div>
        <div v-if="contentType === contentTypes.CUSTOM" class="mb-3">
            <label class="form-label">Files</label>
            <InputSelectOrUploadMedia
                ref="fileInput"
                :currentVal="getMediaId(formData.sections[2])"
                :mediaTypes="[contentTypes.FILE]"
                :isMultiUpload="true"
                @selectedMediaNew="setSectionVal($event, 2, true)"
                @selectedMediaExisting="setSectionVal($event, 2, false)"
            />
        </div>
    </BaseModal>
</template>
<script>
import {CONTENT_TYPES, SEVERITY} from '../../globalData';
import BaseModal from './BaseModal.vue';
import dataUtil from "../../utils/data";
import InputSelectOrUploadMedia from '../inputs/InputSelectOrUploadMedia.vue';
import InputWsiwyg from '../inputs/InputWsiwyg.vue';
import mediaSelectize from "../selectizeCfgs/media";
import InfoToolTip from "../components/InfoToolTip";

const SECTIONS = [
    {type: null, isRequired: true},
    {type: CONTENT_TYPES.TEXT, isRequired: true},
    {type: CONTENT_TYPES.FILE, isRequired: false}
]

export default {
    extends: BaseModal,
    data() {
        return {
            modalName: 'editMediaModal',
            crudUrl: 'user-profile/content-item/',
            isUpdateData: true,
            contentTypes: CONTENT_TYPES,
            formData: this.getEmptyFormData(),
            requiredFields: {
                title: null
            },
            mediaFields: new Set(),  // Dynamically update based on input
        }
    },
    inheritAttrs: false,
    props: ['isContentOnly', 'defaultContentType'],
    components: {InfoToolTip, BaseModal, InputSelectOrUploadMedia, InputWsiwyg},
    computed: {
        allowedBannerMediaTypes() {
            return (this.contentType === CONTENT_TYPES.VIDEO) ? [CONTENT_TYPES.VIDEO] : [CONTENT_TYPES.VIDEO, CONTENT_TYPES.IMAGE];
        },
        contentType() {
            return this.formData.type || this.defaultContentType;
        },
        sectionsLength() {
            return (this.contentType === this.contentTypes.CUSTOM) ? 3 : 2;
        }
    },
    methods: {
        getMediaId(sectionItem) {
            if (!sectionItem) {
                return null;
            }
            return mediaSelectize.getCompositeId(sectionItem.type, sectionItem.value)
        },
        getEmptyFormData() {
            return {
                sections: SECTIONS.map((s) => {
                    return {
                        type: s.type,
                        value: null,
                        mediaKey: null
                    }
                })
            };
        },
        isGoodFormFields(formData) {
            for(let i = 0; i < this.sectionsLength; i++) {
                if(SECTIONS[i].isRequired && dataUtil.isNil(formData.sections[i])) {
                    this.addPopover($(SECTIONS[i].el),
                        {severity: SEVERITY.WARN, content: 'This section is required', isOnce: true}
                    );
                    return false;
                }
            }
            return true;
        },
        processFormData() {
            return Object.assign(this.readForm(), {
                userId: this.initData.user.id,
                profileId: (this.initData.sections) ? this.initData.id : null
            });
        },
        processRawData(rawData) {
            if (!rawData) {
                return this.getEmptyFormData();
            }
            rawData.sections = rawData.sections.map((s) => {
                if (!s.item) {
                    return {
                        type: CONTENT_TYPES.TEXT,
                        value: s.text,
                        mediaKey: null
                    };
                }
                return {
                    type: s.item.type,
                    value: s.item.id,
                    mediaKey: null
                }
            });
            return rawData;
        },
        setSectionVal(val, idx, isNew) {
            const mediaKey = `media-${idx}`;
            const sectionItemData = this.formData.sections[idx];
            if(isNew) {
                this.formData[mediaKey] = val;  // Add the media item to the form to be saved as media
                sectionItemData.mediaKey = mediaKey;  // Add a reference to the media key so it can be found when saving
                sectionItemData.value = null;  // Remove any references to an existing media item
                this.mediaFields.add(mediaKey);
                if (val.type.includes(CONTENT_TYPES.IMAGE)) {
                    sectionItemData.type = CONTENT_TYPES.IMAGE;
                } else if (val.type.includes(CONTENT_TYPES.VIDEO)) {
                    sectionItemData.type = CONTENT_TYPES.VIDEO;
                } else {
                    sectionItemData.type = CONTENT_TYPES.FILE;
                }
            } else {
                delete this.formData[mediaKey];  // Remove the new media item if it exists
                sectionItemData.type = val.type;
                sectionItemData.value = val.id;
                sectionItemData.mediaKey = null;
                this.mediaFields.delete(mediaKey);
            }
        }
    },
    mounted() {
        this.requiredFields.title = this.$refs.title;
        [this.$refs.mediaInput, this.$refs.description, this.$refs.fileInput].forEach((ref, idx) => {
            if (ref) {
                SECTIONS[idx].el = ref.$el;
            }
        });
    }
}
</script>