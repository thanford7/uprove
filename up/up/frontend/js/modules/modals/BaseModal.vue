<template>
    <div class="modal fade" :id="modalId" tabindex="-1" aria-hidden="true">
        <div 
            class="modal-dialog modal-dialog-centered"
            :class="modalClasses"
        >
            <div class="modal-content">
                <div v-if="modalTitle" class="modal-header">
                    <h4 class="modal-title">{{modalTitle}}</h4>
                    <slot name="headerHtml"></slot>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div v-if="headerSubtext" class="modal-body-banner modal-body-banner--top">{{headerSubtext}}</div>
                    <slot/>
                </div>
                <div v-if="!isFooterHidden" class="modal-footer">
                    <button v-if="isAllowDelete" type="button" class="btn btn-danger" @click="$emit('deleteObject', $event)" title="Delete">
                        <font-awesome-icon :icon="['fas', 'trash']" class="-color-white-fa"/>
                    </button>
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button v-if="!isReadOnly" @click="$emit('saveChange', $event)" type="button" class="btn btn-primary">{{primaryButtonText || 'Save changes'}}</button>
                </div>
            </div>
        </div>
    </div>
</template>
<script>

export default {
    props: [
        'modalId', 'modalTitle', 'headerSubtext', 'primaryButtonText', 'isReadOnly', 'isScrollable',
        'isFooterHidden', 'isLargeDisplay', 'isAllowDelete'
    ],
    computed: {
        modalClasses() {
            const classes = [];
            if (this.isScrollable) {
                classes.push('modal-dialog-scrollable');
            }
            if (this.isLargeDisplay) {
                classes.push('modal-lg');
            }
            return classes.join(' ');
        }
    },
}
</script>