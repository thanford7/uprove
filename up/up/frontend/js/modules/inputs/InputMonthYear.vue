<template>
    <div class="input-group" :id="_uid">
        <input type="text" aria-label="Month" class="form-control month" placeholder="MM" :value="month" @blur="updateMonth">
        <input type="text" aria-label="Year" class="form-control year" placeholder="YYYY" :value="year" @blur="updateYear">
    </div>
</template>
<script>
import dataUtil from '../../utils/data';

export default {
    data() {
        return {
            el$: null,
            monthInput$: null,
            yearInput$: null
        }
    },
    props: {
        value: {
            type: [Object, String],  // Should be a dayjs instance
            default: () => dayjs()
        }
    },
    computed: {
        month() {
            if (this.value) {
                return dataUtil.convertToDayJS(this.value).format('MM');
            }
            return null;
        },
        year() {
            if (this.value) {
                return dataUtil.convertToDayJS(this.value).format('YYYY');
            }
            return null;
        }
    },
    methods: {
        updateYear(e) {
            const val = parseInt(e.target.value);
            if (!val || val < 1900 || val > dayjs().year() + 10) {
                this.yearInput$.val(null);
            }
            this.$emit('input', this.value.year(val));
        },
        updateMonth(e) {
            const val = parseInt(e.target.value);
            if (!val || val < 1 || val > 12) {
                this.monthInput$.val(null);
            }
            // dayjs month index is 0-11
            this.$emit('input', this.value.month(val - 1));
        },
    },
    mounted() {
        if (!this.el$) {
            this.el$ = $(`#${this._uid}`);
            this.monthInput$ = this.el$.find('.month');
            this.yearInput$ = this.el$.find('.year');
        }
    }
}
</script>