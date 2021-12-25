<template>
    <select :id="elId || _uid" :placeholder="placeholder"></select>
</template>
<script>
import dataUtil from '../../utils/data';

export default {
    data() {
        return {
            elSel: null,
            targetEl: null  // Select element is not displayed so we need to target an inner html element
        }
    },
    props: ['cfg', 'elId', 'isParseAsInt', 'isParseAsBits', 'placeholder', 'items'],
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
            if (this.items) {
                this.cfg.items = this.items;
            }
            this.elSel = el$.selectize(this.cfg)[0].selectize;
            this.targetEl = el$.next('.selectize-control')[0];

            this.elSel.on('change', () => {
                let val = this.elSel.getValue();
                if (this.isParseAsInt || this.isParseAsBits) {
                    val = this.parseInteger(val);
                }
                if (this.isParseAsBits && Array.isArray(val)) {
                    val = dataUtil.sum(val);
                }
                this.$emit('selected', val);
            });
        }
    }
}
</script>