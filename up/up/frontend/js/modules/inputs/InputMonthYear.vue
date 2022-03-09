<template>
    <div class="input-group" :id="elId">
        <input type="text" aria-label="Month" class="form-control month" placeholder="MM" :value="month" @change="updateMonth">
        <input type="text" aria-label="Year" class="form-control year" placeholder="YYYY" :value="year" @change="updateYear">
    </div>
</template>
<script>
import dataUtil from '../../utils/data';
import dateUtil from '../../utils/dateUtil';

export default {
    data() {
        return {
            el$: null,
            elId: this.getNewElUid(),
            monthInput$: null,
            yearInput$: null,
            month: null,
            year: null,
            internalDate: dateUtil.today().date(1)
        }
    },
    props: ['value'],
    watch: {
        value(newVal) {
            if (!newVal) {
                return;
            }
            newVal = dataUtil.convertToDayJS(newVal);
            this.month = newVal.format('MM');
            this.year = newVal.format('YYYY');
            this.internalDate.month(this.month);
            this.internalDate.year(this.year);
        }
    },
    methods: {
        updateYear(e) {
            e.stopPropagation();
            const val = parseInt(e.target.value);
            if (!val || val < 1900 || val > dateUtil.now().year() + 10) {
                this.yearInput$.val(null);
            }
            this.internalDate = this.internalDate.year(val);
            this.emitChange();
        },
        updateMonth(e) {
            e.stopPropagation();
            const val = parseInt(e.target.value);
            if (!val || val < 1 || val > 12) {
                this.monthInput$.val(null);
            }
            this.internalDate = this.internalDate.month(val - 1); // dayJS starts at index 0
            this.emitChange();
        },
        emitChange() {
            const isGoodDate = parseInt(this.yearInput$.val()) && parseInt(this.monthInput$.val());
            if (isGoodDate) {
                this.$emit('change', dateUtil.serializeDate(this.internalDate));
            }
        },
        initInput() {
            this.el$ = $(`#${this.elId}`);
            if (this.el$.length) {
                this.monthInput$ = this.el$.find('.month');
                this.yearInput$ = this.el$.find('.year');
            }
        }
    },
    mounted() {
        this.initInput();
    },
    updated() {
        this.initInput();
    }
}
</script>