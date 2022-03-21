<template>
    <div class="card-pricing" :class="(canFlip) ? 'card-pricing-flip' : ''">
        <div class="card-side card-side--front">
            <div class="card-side__inner">
                <div class="card-top">
                    <h5 :class="classTextColor"><slot name="front-header"></slot></h5>
                    <p><slot name="front-header-explainer"></slot></p>
                </div>
                <div class="card-price">
                    <slot name="front-price"></slot>
                </div>
                <div class="card-details">
                    <slot name="front-details"></slot>
                </div>
            </div>
            <button class="btn" :class="classBackgroundColor" @click="buttonClickFn">
                <h5><slot name="front-btn-text"></slot></h5>
            </button>
        </div>
        <div class="card-side card-side--back" :class="`card-side--back-${colorScheme}`">
            <div class="card-side__inner">
                <div class="card-price">
                    <h1><slot name="back-price"></slot></h1>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "CardPricing",
    computed: {
        classTextColor() {
            return `-color-${this.colorScheme}-text`;
        },
        classBackgroundColor() {
            return `-color-${this.colorScheme}`;
        }
    },
    props: ['colorScheme', 'canFlip', 'buttonClickFn']
}
</script>