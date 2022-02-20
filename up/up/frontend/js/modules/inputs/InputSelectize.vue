<template>
    <select :id="elId" :placeholder="placeholder"></select>
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
    watch: {
        items(newVal) {
            if (this.elSel) {
                newVal = Array.isArray(newVal) ? newVal : [newVal]
                newVal.forEach((val) => { this.elSel.addItem(val, true); })
            }
        }
    },
    props: ['cfg', 'elId', 'isParseAsInt', 'isParseAsBits', 'placeholder', 'items'],
    methods: {
        parseInteger(val) {
            if (Array.isArray(val)) {
                return val.map((v) => parseInt(v));
            }
            return parseInt(val);
        },
        initSelectize() {
            const el$ = $(`#${this.elId}`);
            if (!this.elSel && el$.length) {
                if (this.items) {
                    this.cfg.items = Array.isArray(this.items) ? this.items : [this.items];
                }
                if (this.cfg.load && !this.cfg.options && this.cfg.items) {
                    this.cfg.options = this.cfg.items;
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
    },
    mounted() {
        this.initSelectize();
    },
    updated() {
        this.initSelectize();
        if (this.items) {
            this.elSel.setValue(this.items, true);
        }
    }
}
</script>