<template>
    <div class="accordion-item">
        <h1 class="accordion-header" :id="`heading-${elId}`">
            <button class="accordion-button" :class="(isOpen) ? '' : 'collapsed'" type="button" data-bs-toggle="collapse"
                    :data-bs-target="`#body-${elId}`" aria-expanded="true"
                    :aria-controls="`body-${elId}`">
                <slot name="header"></slot>
            </button>
        </h1>
        <div :id="`body-${elId}`" class="accordion-collapse collapse" :class="(isOpen) ? 'show' : ''"
             :aria-labelledby="`heading-${elId}`" :data-bs-parent="`#${accordionElId}`">
            <div class="accordion-body">
                <slot name="body"></slot>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "AccordionItem.vue",
    props: ['accordionElId', 'elId', 'isOpen'],
}
</script>