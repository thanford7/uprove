<template>
    <select :id="elId || _uid" :placeholder="placeholder"></select>
</template>
<script>
export default {
    data() {
        return {
            elSel: null
        }
    },
    watch: {
        currentItem(newVal) {
            this.elSel.addItem(newVal, true);
        }
    },
    props: ['currentItem', 'elId', 'placeholder', 'cfg'],
    mounted() {
        if(!this.elSel) {
            this.elSel = $(`#${this.elId || this._uid}`).selectize(this.cfg)[0].selectize;

            this.elSel.on('change', () => {
                this.$emit('selected', this.elSel.getValue());
            });
        }

        if (this.currentItem) {
            this.elSel.addItem(this.currentItem, true);
        }
    }
}
</script>