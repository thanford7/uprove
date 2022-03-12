<template>
    <BaseModal
        :modalId="modalName"
        modalTitle="Record a new video"
    >
        <CustomVideo :isModal="true"
                     :addFormData="{projectId: formData.id}"
                     :targetInitDataKey="[
                         () => initData.userProjects.find((up) => up.id === formData.id).videos,
                         'user.videos'
                     ]"
                     :isUpdateProject="true"
                     @videoComplete="formData.videos.push($event)"
        />
        <template v-slot:footer>
            <button type="button"
                    class="btn btn-secondary"
                    @click="eventBus.emit('open:editUserProjectModal', formData)"
                    data-bs-dismiss="modal"
            >
                <i class="fas fa-arrow-left"></i>&nbsp;Back to edit project
            </button>
        </template>
    </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal";
import CustomVideo from "../components/CustomVideo";

export default {
    name: "AddVideoRecordingModal",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal, CustomVideo},
    data() {
        return {
            modalName: 'addVideoRecordingModal',
        }
    },
}
</script>