<template>
    <InputSelectize
        ref="sel"
        :elId="getNewElUid()"
        :cfg="cfg"
        placeholder="Select content item"
        @selected="emitValue($event)"
    />
</template>
<script>
import {CONTENT_TYPES} from '../../globalData';
import contentUtil from "../../utils/content";
import dataUtil from '../../utils/data';
import InputSelectize from "./InputSelectize";

export default {
    data() {
        return {
            contentSel: null,
            compositeDelimiter: '-'
        }
    },
    props: ['assets'],
    computed: {
        cfg() {
            if (!this.assets) {
                return {};
            }
            const optgroups = [];
            const options = [CONTENT_TYPES.EDUCATION, CONTENT_TYPES.EXPERIENCE, CONTENT_TYPES.CUSTOM, CONTENT_TYPES.PROJECT].reduce((allContent, contentType) => {
                const content = this.assets[contentType];
                // Add grouping
                if (content.length) {
                    optgroups.push({groupName: dataUtil.capitalize(contentType), groupValue: contentType})
                }
                // Add each option
                content.forEach((item) => {
                    item.title = contentUtil.getContentTitle(item);
                    item.compositeId = `${contentType}${this.compositeDelimiter}${item.id}`; // Required because content types can have overlapping IDs
                    allContent.push(item);
                });
                return allContent;
            }, []);
            return {
                options,
                valueField: 'compositeId',
                labelField: 'title',
                searchField: ['title'],
                optgroups,
                optgroupField: 'type',
                optgroupValueField: 'groupValue',
                optgroupLabelField: 'groupName',
                maxItems: 1,
                closeAfterSelect: true
            };
        }
    },
    components: {
        InputSelectize
    },
    methods: {
        emitValue(compositeId) {
            const [contentType, id] = compositeId.split(this.compositeDelimiter);
            this.$emit('selectedContent', {contentType, id: parseInt(id)});
        }
    }
}
</script>