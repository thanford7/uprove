<template>
    <BaseModal
        :modalId="modalName"
        :modalTitle="(formData.id) ? `Edit template: ${formData.title}`: 'Create new template'"
        :primaryButtonText="(formData.id) ? 'Save changes' : 'Create template'"
        :isLargeDisplay="true"
        @saveChange="saveChange($event)"
        @deleteObject="deleteObject($event)"
    >
        <div class="mb-3">
            <label for="templateJobTitle" class="form-label">Title</label>
            <input type="text" class="form-control" placeholder="Required" id="templateJobTitle"
                   v-model="formData.title">
        </div>
        <div class="mb-3">
            <label for="templateJobDescription" class="form-label">Description</label>
            <InputWsiwyg v-model="formData.description" elId="templateJobDescription" placeholder="Add description..."/>
        </div>
    </BaseModal>
</template>

<script>
import {SEVERITY} from '../../globalData';
import BaseModal from "./BaseModal";
import formChecker from "../../utils/form";
import InputWsiwyg from "../inputs/InputWsiwyg";
import $ from "jquery";

export default {
    name: "EditJobTemplateModal",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal, InputWsiwyg},
    data() {
        return {
            modalName: 'editJobTemplateModal',
            crudUrl: 'job-template/',
            isUpdateData: true,
            initDataKey: 'jobTemplates',
            requiredFields: {
                title: '#templateJobTitle',
            },
        }
    },
    methods: {
        isGoodFormFields(formData) {
            if (formChecker.isEmptyWysiwyg(formData.description)) {
                this.addPopover($('#templateJobDescription'),
                    {severity: SEVERITY.WARN, content: 'Description is required', isOnce: true}
                );
                return false;
            }
            return true;
        }
    }
}
</script>