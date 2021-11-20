<template>
    <select :id="elId || _uid" :placeholder="placeholder"></select>
</template>
<script>
export default {
    data() {
        return {
            elSel: null,
            targetEl: null  // Select element is not displayed so we need to target an inner html element
        }
    },
    props: ['elId', 'placeholder', 'cfg', 'isParseAsInt'],
    methods: {
        parseInteger(val) {
            if (Array.isArray(val)) {
                return val.map((v) => parseInt(v));
            }
            return parseInt(val);
        }
    },
    mounted() {
        if(!this.elSel) {
            const el$ = $(`#${this.elId || this._uid}`);
            this.elSel = el$.selectize(this.cfg)[0].selectize;

            this.elSel.on('change', () => {
                const val = this.elSel.getValue();
                this.$emit('selected', (this.isParseAsInt) ? this.parseInteger(val) : val);
            });

            this.targetEl = el$.siblings('.selectize-control')[0]
        }
    }
}
</script>