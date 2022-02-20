<template>
    <div class="progress">
      <div
          class="progress-bar"
          :class="getColorClass()"
          role="progressbar"
          :style="getWidth()"
          :aria-valuenow="pctComplete"
          aria-valuemin="0"
          aria-valuemax="100"
          :title="hoverText"
      >
          <span class="-color-white-text">{{text}}</span>
      </div>
    </div>
</template>

<script>
export default {
    name: "ProgressPill",
    props: ['pctComplete', 'bsColor', 'color', 'text', 'hoverText'],
    methods: {
        getColorClass() {
            if (this.bsColor) {
                return `bg-${this.bsColor}`;
            } else {
                return `-color-${this.color}`;
            }
        },
        getWidth() {
            return `width: ${this.pctComplete}%;`
        }
    }
}
</script>