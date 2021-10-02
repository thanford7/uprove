<template>
    <select :id="elId || _uid" :placeholder="placeholder"></select>
</template>
<script>
import {mapState} from 'vuex';

export default {
    data() {
        return {
            mediaSel: null
        }
    },
    props: {
        currentMediaIds: {
            type: Array
        },
        isMultiUpload: {
            type: Boolean
        },
        placeholder: {
            type: String
        },
        mediaTypes: {
            type: Array,
            required: true
        },
        elId: {
            type: String
        }
    },
    computed: mapState({
        media(state) {
            const re = new RegExp(`^(${this.mediaTypes.join('|')}).*$`);
            const mediaItems = state.media.filter((mediaItem) => mediaItem.type.match(re));
            if (this.mediaSel) {
                this.mediaSel.addOption(mediaItems);
            }
            return mediaItems;
        }
    }),
    watch: {
        currentMediaIds(newVal) {
            this.mediaSel.clear();
            if (newVal && newVal.length) {
                newVal.forEach((val) => { this.mediaSel.addItem(val); });
            }
        }
    },
    methods: {
        getValue() {
            if (this.isMultiUpload) {
                return this.mediaSel.getValue().map((val) => parseInt(val));
            }
            return parseInt(this.mediaSel.getValue());
        },
        createSelectize() {
            const optgroups = _.uniqBy(this.media.map((mediaItem) => ({groupName: _.capitalize(mediaItem.type), groupValue: mediaItem.type})), 'groupName');
            this.mediaSel = $(`#${this.elId || this._uid}`).selectize({
                options: this.media,
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
            })[0].selectize;

            this.mediaSel.on('change', () => {
                this.$emit('selected', this.getValue());
            });

            if (this.currentMediaIds && this.currentMediaIds.length) {
                this.currentMediaIds.forEach((val) => { this.mediaSel.addItem(val, true); });
            }
        }
    },
    mounted() {
        this.createSelectize();
    }
}
</script>