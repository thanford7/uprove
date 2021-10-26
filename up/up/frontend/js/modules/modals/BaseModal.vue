<template>
    <div class="modal fade" :id="modalId" tabindex="-1" aria-hidden="true">
        <div 
            class="modal-dialog modal-dialog-centered"
            :class="modalClasses"
        >
            <div class="modal-content">
                <div class="modal-header">
                    <h4 class="modal-title">{{modalTitle}}</h4>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div v-if="headerSubtext" class="modal-body-banner modal-body-banner--top">{{headerSubtext}}</div>
                    <slot/>
                </div>
                <div v-if="!isFooterHidden" class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button v-if="!isReadOnly" @click="$emit('saveChange')" type="button" class="btn btn-primary" data-bs-dismiss="modal">{{primaryButtonText || 'Save changes'}}</button>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import {mapState} from 'vuex';

export default {
    props: ['modalId', 'modalTitle', 'headerSubtext', 'primaryButtonText', 'isReadOnly', 'isScrollable', 'isFooterHidden', 'isLargeDisplay'],
    data() {
        return {
            baseUrl: 'api/v1/',
            crudUrl: null
        }
    },
    computed: {
        ...mapState({
            eventBus: 'eventBus'
        }),
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
    methods: {
        readForm() {
            // subclass
        },
        hookEvents() {
            // subclass
        },
        isGoodFormData(formData) {
            return true;
            // subclass
        },
        processFormData(formData) {
            // subclass
            return formData;
        },
        onSaveSuccess(requestData, responseData) {
            // subclass
        },
        superSaveChange(cfg = {}) {
            const formData = this.readForm();
            const requestData = this.processFormData(formData);
            if(!this.isGoodFormData(formData)) {
                return;
            }

            $.ajax(Object.assign({
                url: this.baseUrl + this.crudUrl,
                method: 'PUT',
                data: JSON.stringify(requestData),
                contentType: 'application/json',
                dataType: 'json',
                success: this.onSaveSuccess
            }, cfg));
        },
    },
    mounted() {
        this.hookEvents();
    }
}
</script>