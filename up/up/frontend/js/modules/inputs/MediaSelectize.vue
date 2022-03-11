<template>
    <InputSelectize
        ref="input"
        :elId="getNewElUid()"
        :cfg="cfg"
        :items="currentVal"
        :placeholder="placeholder"
        @selected="$emit('selectedMedia', parseVal($event))"
    />
</template>
<script>
import dataUtil from '../../utils/data';
import InputSelectize from "./InputSelectize";
import mediaSelectize from "../selectizeCfgs/media";

export default {
    components: {InputSelectize},
    props: {
        isMultiUpload: Boolean,
        placeholder: String,
        currentVal: [String, Number],
        mediaTypes: {
            type: Array,
            required: true
        },
        assetsKey: {
            type: String,
            default: 'assets'
        }
    },
    computed: {
        cfg() {
            const optgroups = [];
            const assets = dataUtil.get(this.initData, this.assetsKey);
            const options = (assets) ? this.mediaTypes.reduce((allMedia, mediaType) => {
                const mediaItems = assets[`${mediaType}s`];
                if (!mediaItems || !mediaItems.length) {
                    return allMedia;
                }
                optgroups.push({groupName: dataUtil.capitalize(mediaType), groupValue: mediaType})
                mediaItems.forEach((item) => {
                    item.compositeId = mediaSelectize.getCompositeId(mediaType, item.id);
                    item.type = mediaType;
                    allMedia.push(item);
                });
                return allMedia;
            }, []) : [];
            return {
                options,
                valueField: 'compositeId',
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
                            return `<div><div class="img"><img src="${item.image}" class="img-thumbnail"><span>${escape(item.title)}</span></div></div>`;
                        } else if (item.type === 'video') {
                            return `<div>
                                        <div class="img">
                                            <video class="img-thumbnail" preload="metadata">
                                                <source src="${item.video}#t=1">
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
    methods: {
        parseVal(val) {
            return mediaSelectize.getParsedCompositeId(val);
        },
    }
}
</script>