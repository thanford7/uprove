<template>
    <InputSelectize
        :elId="getNewElUid()"
        ref="sel"
        placeholder="Status"
        :cfg="{
            plugins: ['remove_button'],
            maxItems: (isMultiSelect) ? null : 1,
            options: applicationOptions
        }"
    />
</template>

<script>
import {APPLICATION_STATUS} from '../../globalData';
import InputSelectize from "./InputSelectize";

export default {
    name: "ApplicationStatusSelectize",
    props: ['excludeStatusOptions', 'isMultiSelect'],
    components: {InputSelectize},
    computed: {
        applicationOptions() {
            return Object.entries(APPLICATION_STATUS).reduce((opts, [key, val]) => {
                if (this.excludeStatusOptions && this.excludeStatusOptions.includes(key)) {
                    return opts;
                }
                opts.push({value: key, text: val});
                return opts;
            }, []);
        },
    },
    methods: {
        setValue(val) {
            this.$refs.sel.elSel.setValue(val);
        }
    }
}
</script>