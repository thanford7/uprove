<template>
    <BaseModal
        :modalId="modalName"
        :isLargeDisplay="true"
        :isReadOnly="true"
        :isFooterHidden="true"
    >
        <div class="d-flex justify-content-end">
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="celebrationLogo mb-3 d-flex justify-content-center">
            <img :src="globalData.STATIC_URL + 'img/favicon.png'">
        </div>
        <h5 v-if="formData" class="mt-4 text-center">
            {{ formData.msg }}
        </h5>
    </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal";
import confetti from "canvas-confetti";

export default {
    name: "CelebrationModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal},
    data() {
        return {
            modalName: 'celebrationModal',
        }
    },
    methods: {
        onModalOpen() {
            confetti({
                particleCount: 100,
                spread: 160
            });
        }
    }
}
</script>