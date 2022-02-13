<template>
    <InputSelectize
        ref="sel"
        :elId="getNewElUid()"
        :cfg="cfg"
        placeholder="Select content item"
        @selected="$emit('selected', $event)"
    />
</template>
<script>
import dataUtil from '../../utils/data';
import InputSelectize from "./InputSelectize";

export default {
    data() {
        return {
            contentSel: null
        }
    },
    computed: {
        cfg() {
            if (!this.assets) {
                return {};
            }
            const optgroups = [];
            const options = ['education', 'experience', 'content'].reduce((allContent, contentType) => {
                const content = this.assets[contentType];
                // Add grouping
                if (content.length) {
                    optgroups.push({groupName: dataUtil.capitalize(contentType), groupValue: contentType})
                }
                // Add each option
                content.forEach((item) => {
                    item.contentType = contentType;
                    item.compositeId = `${contentType}-${item.id}`; // Required because content types can have overlapping IDs
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
                optgroupField: 'contentType',
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
    props: ['section', 'assets'],
}
</script>