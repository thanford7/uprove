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
    props: [
        'cfg', 'elId', 'isParseAsInt', 'isParseAsBits', 'placeholder', 'items',
        'isPreserveValue'  // Don't clear the selectize on form clear event
    ],
    methods: {
        clear() {
            this.elSel.clear(true);
        },
        parseInteger(val) {
            if (Array.isArray(val)) {
                return val.map((v) => parseInt(v));
            }
            return parseInt(val);
        },
        parseSelVal() {
            let val = this.elSel.getValue();
            if (this.isParseAsInt || this.isParseAsBits) {
                val = this.parseInteger(val);
            }
            if (this.isParseAsBits && Array.isArray(val)) {
                val = dataUtil.sum(val);
            }
            // Make sure null values and empty arrays are not included
            if (Array.isArray(val)) {
                val = val.filter((v) => !dataUtil.isNil(v));
                if (!val.length) {
                    val = null;
                }
            }
            return val;
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
                this.targetEl = el$.next('.selectize-control').find('.selectize-input')[0];

                this.elSel.on('change', () => {
                    this.$emit('selected', this.parseSelVal());
                });
                this.elSel.on('blur', () => { $(this.targetEl).trigger('blur'); });
                this.eventBus.on('formClear', () => {
                    if (!this.isPreserveValue) {
                        this.clear();
                    }
                });
            }
        },
        resetOptions(options) {
            let currentItems = this.elSel.getValue();
            currentItems = (Array.isArray(currentItems)) ? currentItems : [currentItems];
            this.elSel.clearOptions(true);
            this.elSel.addOption(options);
            this.elSel.refreshOptions(false);

            // Try resetting selected values if they are still available options
            currentItems.forEach((i) => {
                this.elSel.addItem(i, true);
            });

            let newItems = this.elSel.getValue();
            newItems = (Array.isArray(newItems)) ? newItems : [newItems];
            if (!dataUtil.isArraysEqual(currentItems, newItems)) {
                this.$emit('selected', this.parseSelVal());
            }
        },
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