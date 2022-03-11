<template>
    <div>
        <slot v-if="isContentOnly"/>
        <div v-else class="modal fade" :id="modalId" tabindex="-1" aria-hidden="true" @keydown="handleKeyPress">
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
                        <BannerAlert/>
                        <div class="container-fluid">
                            <slot v-if="!isContentOnly"/>
                        </div>
                    </div>
                    <div v-if="!isFooterHidden" class="modal-footer">
                        <slot name="footer">
                            <ButtonDelete v-if="isAllowDelete" class="-pull-left" @click="$emit('deleteObject', $event)"/>
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button v-if="!isReadOnly" @click="$emit('saveChange', $event)" type="button" class="btn btn-primary">{{primaryButtonText || 'Save changes'}}</button>
                        </slot>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import BannerAlert from "../components/BannerAlert";
import ButtonDelete from "../buttons/ButtonDelete";
import Modal from "bootstrap/js/dist/modal";
import dataUtil from "../../utils/data";

export default {
    components: {BannerAlert, ButtonDelete},
    props: [
        'modalId', 'modalTitle', 'headerSubtext', 'primaryButtonText', 'isReadOnly', 'isScrollable',
        'isFooterHidden', 'isLargeDisplay', 'isFullScreenDisplay', 'isAllowDelete', 'isContentOnly'
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
            if (this.isFullScreenDisplay) {
                classes.push('modal-fullscreen-xl-down');
            }
            return classes.join(' ');
        }
    },
    methods: {
        handleKeyPress(e) {
            if (e.keyCode !== 13) {
                return;
            }
            const target$ = $(e.target);
            const isIgnoreEnter = target$.hasClass('ProseMirror') || target$.is('textarea') || target$.parent('.selectize-input').length;
            // Save on enter
            if (!isIgnoreEnter  && $(`#${this.modalId} .btn-primary`).length) {
                e.preventDefault();
                this.$emit('saveChange', e);
            }
        },
        initModal() {
            const modal$ = $(`#${this.modalName}`);
            if (modal$.length) {
                Modal.getOrCreateInstance(modal$, {backdrop: 'static'});
                modal$[0].addEventListener('hidden.bs.modal', (e) => {
                    this.eventBus.emit('formClear');  // Clear all non-reactive elements
                });
            }
        }
    },
    mounted() {
        this.initModal();
        if (this.isContentOnly) {
            this.eventBus.on('ajaxSuccess', this.initForm);
        }
        this.eventBus.on('injectFormData', ([modalName, injectFn, dataTargetPath]) => {
            if (this.modalName === modalName && this.formData) {
                const target = dataUtil.get(this.formData, dataTargetPath);
                injectFn(target);
            }
        });
    },
    updated() {
        this.initModal();
    }
}
</script>