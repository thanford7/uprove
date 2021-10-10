<template>
    <select id="selectContent"></select>
</template>
<script>
import {mapState} from 'vuex';

export default {
    data() {
        return {
            contentSel: null
        }
    },
    props: ['contentSection', 'currentContentIds'],
    computed: mapState({
        selectedContentIds(state) { return (this.contentSection === 'highlight') ? state[`${this.contentSection}Ids`] : this.currentContentIds || []; },
        content: 'content',
        eventBus: 'eventBus'
    }),
    watch: {
        // Update available content options after a user adds/removes content
        selectedContentIds(newVal, oldVal) {
            const options = this.getContentOptions();
            this.contentSel.clear(true); // Clear existing selected options
            this.contentSel.clearOptions(true);
            this.contentSel.addOption(options);
            this.handleNoOptions(options);
        }
    },
    methods: {
        getContentOptions() {
            return Object.values(this.content).filter((contentItem) => !this.selectedContentIds.includes(contentItem.ID));
        },
        getSelectedContentId() {
            return this.contentSel.getValue();
        },
        handleNoOptions(options) {
            if (options.length) {
                this.contentSel.enable();
                this.contentSel.settings.placeholder = 'Select content';
            } else {
                this.contentSel.settings.placeholder = 'No content available';
                this.contentSel.disable();
            }
            this.contentSel.updatePlaceholder();
        }
    },
    mounted() {
        if(!this.contentSel) {
            const options = this.getContentOptions();
            const optgroups = _.uniqBy(options.map((option) => ({groupName: _.capitalize(option.post_type), groupValue: option.post_type})), 'groupValue');
            this.contentSel = $('#selectContent').selectize({
                options,
                valueField: 'ID',
                labelField: 'post_title',
                searchField: ['post_title'],
                optgroups,
                optgroupField: 'post_type',
                optgroupValueField: 'groupValue',
                optgroupLabelField: 'groupName',
                maxItems: 1,
                closeAfterSelect: true
            })[0].selectize;

            this.handleNoOptions(options);

            this.contentSel.on('change', () => {
                this.$emit('selected', this.getSelectedContentId());
            });
        }
    }
}
</script>