<template>
    <BaseModal
        :modalId="modalName"
        :modalTitle="getModalTitle()"
        :isLargeDisplay="true"
        :isScrollable="true"
    >
        <template v-slot:headerHtml>
            &nbsp;
            <span v-if="formData.evaluationCriteria && formData.evaluationCriteria.length"
                  class="badge rounded-pill"
                  :class="`bg-${getBadgeColor({score: formData.evaluationScorePct})}`"
                  style="font-size: 1em;"
            >
                {{formData.evaluationScorePct}}%
            </span>
        </template>
        <div class="row">
            <div :class="(isShowEvaluation) ? 'col-md-6' : 'col'">
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
            <div v-if="isShowEvaluation" class="col-md-6">
                <div v-if="!hasEvaluated && !isAddEvaluation">
                    <a href="#" @click="isAddEvaluation = true">
                        <i class="fas fa-plus-circle"></i> Add evaluation
                    </a>
                </div>
                <div v-if="isAddEvaluation">
                    <div>
                        <span class="-text-bold">Evaluation Guide&nbsp;</span>
                        <span
                            class="badge rounded-pill"
                            :class="`bg-${getBadgeColor({evalCriteria: evals})}`"
                        >{{getEvaluationScore(evaluationCriteriaTemplate)}}%</span>
                    </div>
                    <div class="row mt-2 mb-2">
                        <div class="col-4 col-md-6 col-lg-5">
                            <div class="-sub-text">0 = Unaddressed</div>
                            <div class="-sub-text">1 = Poorly addressed</div>
                        </div>
                        <div class="col-4 col-md-6 col-lg-5">
                            <div class="-sub-text">2 = Addressed</div>
                            <div class="-sub-text">3 = Excellent</div>
                        </div>
                    </div>
                    <div v-for="criterion in evaluationCriteriaTemplate" class="row mb-2">
                        <div class="col-2 col-md-3 col-lg-2">
                            <input type="number"
                               class="form-control form-control-sm"
                               placeholder="0" min="0" max="3"
                               style="display: inline-block; width: fit-content;"
                               @change="criterion.value = parseInt($event.target.value)"
                            >
                        </div>
                        <div class="col-10 col-md-9 col-lg-10">
                            {{criterion.criterion}}
                        </div>
                    </div>
                </div>
                <div v-for="evals in formData.evaluationsByUserId">
                    <div>
                        <span class="-text-bold">{{getEvaluatorLabel(evals[0])}}&nbsp;</span>
                        <span
                            class="badge rounded-pill"
                            :class="`bg-${getBadgeColor({evalCriteria: evals})}`"
                        >{{getEvaluationScore(evals)}}%</span>
                    </div>
                    <div class="row mt-2 mb-2">
                        <div class="col-4 col-md-6 col-lg-5">
                            <div class="-sub-text">0 = Unaddressed</div>
                            <div class="-sub-text">1 = Poorly addressed</div>
                        </div>
                        <div class="col-4 col-md-6 col-lg-5">
                            <div class="-sub-text">2 = Addressed</div>
                            <div class="-sub-text">3 = Excellent</div>
                        </div>
                    </div>
                    <div v-for="evaluation in evals" class="row mb-2">
                        <div class="col-2 col-md-3 col-lg-2">
                            <input type="number"
                               class="form-control form-control-sm"
                               placeholder="0" min="0" max="3"
                               style="display: inline-block; width: fit-content;"
                               :value="evaluation.value"
                               :disabled="!isEvaluatorSelf(evaluation)"
                               @change="evaluation.value = parseInt($event.target.value)"
                            >
                        </div>
                        <div class="col-10 col-md-9 col-lg-10">
                            {{evaluation.evaluationCriterion.criterion}}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <template v-slot:footer>
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="$emit('approve', formData.application)">
                <i class="far fa-thumbs-up -color-green-text"></i> Approve <InfoToolTip :elId="getNewElUid()" :content="TOOLTIPS.employerApprove"/>
            </button>
            <button @click="$emit('decline', formData.application)" data-bs-dismiss="modal" type="button" class="btn btn-secondary">
                <i class="far fa-thumbs-down -color-red-text"></i> Decline <InfoToolTip :elId="getNewElUid()" :content="TOOLTIPS.employerDecline"/>
            </button>
            <button v-if="isAddEvaluation || hasEvaluated" @click="saveChange" type="button" class="btn btn-primary">
                Save evaluation
            </button>
        </template>
    </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal";
import dataUtil from "../../utils/data";
import FileDisplay from "../components/FileDisplay";
import formChecker from '../../utils/form';
import InfoToolTip from "../components/InfoToolTip";
import InputCheckBox from "../inputs/InputCheckBox";
import InputSelectize from "../inputs/InputSelectize";
import userProjectUtil from "../../utils/userProject";

export default {
    name: "ViewCandidateApplicationModal",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal, FileDisplay, InfoToolTip, InputCheckBox, InputSelectize},
    computed: {
        evaluationCriteriaTemplate() {
            if (!this.formData || dataUtil.isEmpty(this.formData)) {
                return [];
            }
            const allEvalCriteria = this.initData.projects.find((p) => p.id === this.formData.customProject.projectId).evaluationCriteria;
            const selectedEvalCriteria = this.initData.customProjectEvaluationCriteria.filter((ec) => ec.customProjectId === this.formData.customProject.id);
            return selectedEvalCriteria.map((criterion) => allEvalCriteria.find((ec) => criterion.evaluationCriterionId === ec.id));
        },
        isShowEvaluation() {
            return (
                this.evaluationCriteriaTemplate.length ||
                (this.formData.evaluationCriteria && this.formData.evaluationCriteria.length)
            )
        },
    },
    data() {
        return {
            modalName: 'viewCandidateApplicationModal',
            crudUrl: 'user-project-evaluation/',
            initDataKey: 'employer',
            isUpdateData: true,
            hasEvaluated: false,  // Whether the current user has submitted an evaluation
            isAddEvaluation: false
        }
    },
    methods: {
        getBadgeColor: userProjectUtil.getBadgeColor,
        getEvaluationScore: userProjectUtil.getEvaluationScore,
        isEmpty: dataUtil.isEmpty,
        isEmptyString: formChecker.isEmptyWysiwyg,
        parseInt: parseInt,
        getModalTitle() {
            if (!this.formData || this.isEmpty(this.formData)) {
                return '';
            }
            return `Application: ${this.formData.user.firstName} ${this.formData.user.lastName}`;
        },
        isEvaluatorSelf(evalItem) {
            return evalItem.evaluator.id === this.globalData.uproveUser.id;
        },
        getEvaluatorLabel(evalItem) {
            const evaluator = evalItem.evaluator;
            const evaluatorName = (this.isEvaluatorSelf(evalItem)) ? 'you' : `${evaluator.firstName} ${evaluator.lastName}`;
            return `Evaluation completed by ${evaluatorName}`;
        },
        processRawData(application) {
            this.hasEvaluated = false;  // Reset when modal is opened
            const userProject = application.userProject;
            this.isAddEvaluation = !userProject.evaluationCriteria.length;  // Add the evaluation template if no evaluation has been completed
            userProject.application = dataUtil.omit(application, ['userProject']);
            const project = this.initData.projects.find((p) => p.id === userProject.customProject.projectId);
            userProject.evaluationCriteria.forEach((ec) => {
                ec.evaluationCriterion = project.evaluationCriteria.find((c) => c.id === ec.evaluationCriterionId);
                this.hasEvaluated = this.hasEvaluated || this.isEvaluatorSelf(ec);
            });
            userProject.evaluationsByUserId = dataUtil.groupByKey(userProject.evaluationCriteria, 'evaluator.id');
            Object.values(userProject.evaluationsByUserId).forEach((evalCriteria) => {
                dataUtil.sortBy(evalCriteria, ['evaluationCriterion.category', 'evaluationCriterionId'], true);
            });
            return userProject;
        },
        processFormData() {
            return {
                userProjectId: this.formData.id,
                evaluatorId: this.globalData.uproveUser.id,
                employerId: this.initData.employer.id,
                evaluationCriteria: (this.hasEvaluated) ? this.formData.evaluationsByUserId[this.globalData.uproveUser.id] : this.evaluationCriteriaTemplate
            }
        },
        getAjaxCfgOverride() {
            return {method: 'PUT'};
        }
    },
    emits: ['approve', 'decline']
}
</script>