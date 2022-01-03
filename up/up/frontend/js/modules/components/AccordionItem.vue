<template>
    <div class="accordion-item">
        <h1 class="accordion-header" :id="headerElId">
            <button class="accordion-button" :class="(isOpen) ? '' : 'collapsed'" type="button" data-bs-toggle="collapse"
                    :data-bs-target="`#${bodyElId}`" aria-expanded="true"
                    :aria-controls="bodyElId">
                <slot name="header"></slot>
            </button>
        </h1>
        <div :id="bodyElId" class="accordion-collapse collapse" :class="(isOpen) ? 'show' : ''"
             :aria-labelledby="headerElId" :data-bs-parent="(isAllowMultipleOpen) ? null : `#${accordionElId}`">
            <div class="accordion-body">
                <slot name="body"></slot>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "AccordionItem.vue",
    props: ['accordionElId', 'elId', 'isOpen', 'isAllowMultipleOpen'],
    computed: {
        headerElId() {
            return `heading-${this.elId}`;
        },
        bodyElId() {
            return `body-${this.elId}`;
        }
    },
    methods: {
        toggleItem(isOpen) {
            $('button.accordion-button').toggleClass('collapsed', isOpen)
        }
    }
}
</script>