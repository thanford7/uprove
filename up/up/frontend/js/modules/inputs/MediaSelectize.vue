<template>
    <InputSelectize
        :elId="getNewElUid()"
        :cfg="cfg"
        :placeholder="placeholder"
        :isParseAsInt="true"
        @selected="$emit('selected', $event)"
    />
</template>
<script>
import dataUtil from '../../utils/data';
import InputSelectize from "./InputSelectize";

export default {
    components: {InputSelectize},
    data() {
        return {
            mediaSel: null
        }
    },
    props: {
        isMultiUpload: {
            type: Boolean
        },
        placeholder: {
            type: String
        },
        mediaTypes: {
            type: Array,
            required: true
        }
    },
    computed: {
        cfg() {
            const optgroups = [];
            const options = this.mediaTypes.reduce((allMedia, mediaType) => {
                const mediaItems = this.initData[`${mediaType}s`];
                if (!mediaItems || !mediaItems.length) {
                    return allMedia;
                }
                optgroups.push({groupName: dataUtil.capitalize(mediaType), groupValue: mediaType})
                mediaItems.forEach((item) => {
                    item.compositeId = `${mediaType}-${item.id}`;
                    item.type = mediaType;
                    allMedia.push(item);
                });
                return allMedia;
            }, []);
            return {
                options,
                valueField: 'id',
                labelField: 'title',
                searchField: ['title'],
                optgroups,
                optgroupField: 'type',
                optgroupValueField: 'groupValue',
                optgroupLabelField: 'groupName',
                maxItems: (this.isMultiUpload) ? null : 1,
                plugins: (this.isMultiUpload) ? ['remove_button'] : [],
                render: {
                    option: (item, escape) => {
                        if (item.type === 'image') {
                            return `<div><div class="img"><img src="${item.guid}" class="img-thumbnail"><span>${escape(item.title)}</span></div></div>`;
                        } else if (item.type === 'video') {
                            return `<div>
                                        <div class="img">
                                            <video class="img-thumbnail" preload="metadata">
                                                <source src="${item.guid}#t=1">
                                            </video>
                                            <span>${escape(item.title)}</span>
                                        </div>
                                    </div>`;
                        } else {
                            return `<div>${escape(item.title)}</div>`;
                        }
                    }
                }
            }
        }
    },
}
</script>