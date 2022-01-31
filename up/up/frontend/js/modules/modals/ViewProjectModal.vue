<template>
    <BaseModal
        :modalId="modalName"
        :modalTitle="formData.title"
        :isFooterHidden="true"
        :isReadOnly="true"
        :isLargeDisplay="true"
    >
        <template v-slot:headerHtml>
            &nbsp;<span class="badge -color-darkblue float-end align-items-center">{{formData.role}}</span>
        </template>
        <div>
            <template v-for="skill in formData.skills">
                <span class="badge -color-lightblue -color-black-text">{{skill.name}}</span>&nbsp;
            </template>
        </div>
        <div class="mb-2">
            <template v-for="skillLevel in formData.skillLevels">
                <span class="badge -color-lightgrey -color-black-text">{{skillLevel}}</span>&nbsp;
            </template>
        </div>
        <div v-html="formData.description"></div>
    </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal";

export default {
    name: "ViewProjectModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal},
    data() {
        return {
            modalName: 'viewProjectModal',
        }
    },
}
</script>