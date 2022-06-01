<template>
    <div class="slidecontainer">
        <div>
            <span v-if="title" class="-color-moderategrey-text">{{title}} ({{ valString }})</span>
        </div>
        <input type="range" :min="min" :max="max" :step="step" class="slider" :id="elId">
    </div>
</template>

<script>

export default {
    name: "RangeSlider",
    props: {
        elId: {
            type: [String],
        },
        min: {
            type: [Number],
            default: 0
        },
        max: {
            type: [Number],
            default: 100
        },
        startingVal: {
            type: [Number],
            default: 0
        },
        title: {
            type: [String, null]
        },
        isPct: {
            type: [Boolean],
            default: true
        },
        step: {
            type: [Number],
            default: 1
        },
        valueFormatFn: {
            type: [Function, null]
        }
    },
    computed: {
        valString() {
            if (this.valueFormatFn) {
                return this.valueFormatFn(this.val);
            }
            if (this.isPct) {
                const pct = Math.round((this.val / this.max) * 100)
                return `${pct}%`;
            }
            return this.val;
        }
    },
    data() {
        return {
            val: this.min
        }
    },
    methods: {
        setValue(val) {
            const slider$ = $(`#${this.elId}`);
            slider$.val(val);
            this.val = val;
            slider$.trigger('change');
        }
    },
    mounted() {
        const slider$ = $(`#${this.elId}`);
        this.setValue(Math.max(this.startingVal, this.min));
        slider$.on('input', (e) => {
            this.val = Number.parseInt(e.currentTarget.value);
        });

        slider$.on('change', (e) => {
            const val = Number.parseInt(e.currentTarget.value);
            this.$emit('changed', val);
        })
    }
}
</script>