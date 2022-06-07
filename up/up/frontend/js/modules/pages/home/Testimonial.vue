<template>
    <div class="testimonial">
        <div class="testimonial__headshot">
            <img
                :src="headshotUrl"
                alt="Headshot"
            >
        </div>
        <div class="testimonial__quote">
            <i class="fas fa-quote-left -color-orange-text"></i>&nbsp;
            <slot/>
        </div>
        <div class="testimonial__name">
            <slot name="name"></slot>
        </div>
        <div class="testimonial__title">
            <slot name="title"></slot>
        </div>
    </div>
</template>

<script>
export default {
    name: "Testimonial",
    props: ['headshotUrl']
}
</script>