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
    computed: {
        ...mapState({
            crudUrl: 'crudUrlProfile',
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
        processFormData(formData, preSaveData) {
            return Object.assign(formData, preSaveData);
        },
        onSaveSuccess(requestData, responseData) {
            // subclass
        },
        getPreSaveChange() {
            return new Promise((resolve, reject) => {
                resolve({});
            });
        },
        saveChange(cfg = {}) {
            const formData = this.readForm();
            if(!this.isGoodFormData(formData)) {
                return;
            }
            const preSave = this.getPreSaveChange();
            preSave.then((preSaveData) => {
                const requestData = this.processFormData(formData, preSaveData);
                const successFn = (responseData) => {
                    this.onSaveSuccess(requestData, responseData);
                };
                this.eventBus.saveContent(this.crudUrl, requestData, Object.assign({
                    success: successFn,
                }, cfg));
            })
        },
    },
    mounted() {
        this.hookEvents();
    }
}
</script>