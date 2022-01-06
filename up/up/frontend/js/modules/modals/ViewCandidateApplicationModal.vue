<template>
    <BaseModal
        :modalId="modalName"
        :modalTitle="getModalTitle()"
        :isLargeDisplay="true"
        :isScrollable="true"
    >
        <div class="row">
            <div :class="(evaluationCriteria.length) ? 'col-md-6' : 'col'">
                <div v-if="!isEmptyString(formData.projectNotes)" class="mb-3">
                    <label class="form-label">Notes</label>
                    <div v-html="formData.projectNotes"></div>
                </div>
                <div v-if="formData.files && formData.files.length" class="mb-3">
                    <label class="form-label">Files</label>
                    <div v-for="file in formData.files">
                        <FileDisplay :file="file"/>
                    </div>
                </div>
                <div v-if="formData.videos && formData.videos.length" class="mb-3">
                    <label class="form-label">Videos</label>
                    <div v-for="video in formData.videos">
                        <video controls>
                          <source :src="video.video">
                        </video>
                    </div>
                </div>
                <div v-if="formData.images && formData.images.length" class="mb-3">
                    <label class="form-label">Images</label>
                    <div v-for="image in formData.images">
                        <img :src="image.image" class="img-thumbnail">
                    </div>
                </div>
            </div>
            <div v-if="evaluationCriteria.length" class="col-md-6">
                <label class="form-label">Evaluation Guide</label>
                <div v-for="criterion in evaluationCriteria" class="form-check">
                    <InputCheckBox
                        :elId="`criterion-${criterion.id}`"
                        :label="criterion.criterion"
                        @click="criterion.isChecked = !criterion.isChecked"
                    />
                </div>
            </div>
        </div>
    </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal";
import dataUtil from "../../utils/data";
import FileDisplay from "../components/FileDisplay";
import formChecker from '../../utils/form';
import InputCheckBox from "../inputs/InputCheckBox";

export default {
    name: "ViewCandidateApplicationModal",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal, FileDisplay, InputCheckBox},
    computed: {
        evaluationCriteria() {
            if (!this.formData || dataUtil.isEmpty(this.formData)) {
                return [];
            }
            const allEvalCriteria = this.initData.projects.find((p) => p.id === this.formData.customProject.projectId).evaluationCriteria;
            const selectedEvalCriteria = this.initData.customProjectEvaluationCriteria.filter((ec) => ec.customProjectId === this.formData.customProject.id);
            return selectedEvalCriteria.map((criterion) => allEvalCriteria.find((ec) => criterion.evaluationCriterionId === ec.id));
        }
    },
    data() {
        return {
            modalName: 'viewCandidateApplicationModal',
        }
    },
    methods: {
        isEmpty: dataUtil.isEmpty,
        isEmptyString: formChecker.isEmptyWysiwyg,
        getModalTitle() {
            if (!this.formData || this.isEmpty(this.formData)) {
                return '';
            }
            return `Application: ${this.formData.user.firstName} ${this.formData.user.lastName}`;
        }
    }
}
</script>