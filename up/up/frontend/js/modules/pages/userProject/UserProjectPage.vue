<template>
    <BasePage>
        <div class="row justify-content-around mt-4">
            <div class="col-md-5 card-custom card-custom--no-side-margin p-0 mt-2">
                <div class="ps-3 pe-3">
                    <h5 class="-skew-top-left">
                        <EvaluationScoreBadge :evalScorePct="userProject.projectEvalScorePct"/>
                    </h5>
                    <h5>{{userProject.user.firstName}} {{userProject.user.lastName}}</h5>
                </div>
                <CollapseDiv v-if="userProject.applications.length" :elId="getNewElUid()" class="mt-2 mb-2">
                    <template v-slot:header>
                        Current job applications
                    </template>
                    <table class="table table-hover">
                        <thead>
                            <tr>
                                <th></th>
                                <th>Job title</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="application in userProject.applications">
                                <td>
                                    <ApplicationDropdownOpts :application="application" :applications="userProject.applications"/>
                                </td>
                                <td>{{application.job.jobTitle}}</td>
                                <td>{{ getApplicationStatus(application) }}</td>
                            </tr>
                        </tbody>
                    </table>
                </CollapseDiv>
                <CollapseDiv :elId="getNewElUid()" class="mt-2">
                    <template v-slot:header>
                        Project submission
                    </template>
                    <div v-if="!isEmptyString(userProject.projectNotes)" class="mb-3">
                        <label class="form-label">Notes</label>
                        <div v-html="userProject.projectNotes"></div>
                    </div>
                    <div v-if="userProject.videos?.length" class="mb-3">
                        <label class="form-label">Videos</label>
                        <div v-for="video in userProject.videos" class="mb-2">
                            <video controls>
                              <source :src="video.video">
                            </video>
                        </div>
                    </div>
                    <div v-if="userProject.images?.length" class="mb-3">
                        <label class="form-label">Images</label>
                        <div v-for="image in userProject.images" class="mb-2">
                            <img :src="image.image" class="img-thumbnail">
                        </div>
                    </div>
                    <div v-if="userProject.files?.length" class="mb-3">
                        <label class="form-label">Files</label>
                        <div v-for="file in filesWithThumbnails" class="mb-2">
                            <div>
                                <FileDisplay :file="file"/>
                            </div>
                            <img :src="file.thumbnail">
                        </div>
                        <div v-for="file in filesWithoutThumbnails" class="mb-2">
                            <FileDisplay :file="file"/>
                        </div>
                    </div>
                </CollapseDiv>
                <CollapseDiv v-if="canEvaluate" :elId="getNewElUid()">
                    <template v-slot:header>
                        Project evaluation
                    </template>
                    <div v-if="userProject?.evaluationCriteria?.length">
                        <div v-if="canEvaluate && !hasEvaluated && !isAddEvaluation" class="mb-2">
                            <a href="#" @click="isAddEvaluation = true">
                                <i class="fas fa-plus-circle"></i> Add evaluation
                            </a>
                        </div>
                        <div v-if="isAddEvaluation" class="mb-2">
                            <div>
                                <span class="-text-bold">Evaluation Guide&nbsp;</span>
                                <span
                                    class="badge rounded-pill"
                                    :class="`bg-${getBadgeColor({evalCriteria: userProject.evaluationCriteria})}`"
                                >{{getEvaluationScore(userProject.evaluationCriteria)}}%</span>
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
                            <div v-for="criterion in userProject.evaluationCriteria" class="row mb-2">
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
                            <button @click="saveEvaluation" type="button" class="btn btn-primary w-100">
                                Save evaluation
                            </button>
                        </div>
                        <div v-for="evals in Object.values(initData.userProject.evaluations)" class="mb-2">
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
                                    {{getEvaluationCriterion(evaluation.evaluationCriterionId).criterion}}
                                </div>
                            </div>
                            <button v-if="isEvaluatorSelf(evals[0])" @click="saveEvaluation" type="button" class="btn btn-primary w-100">
                                Save evaluation
                            </button>
                        </div>
                    </div>
                </CollapseDiv>
            </div>
            <ProjectAccordion
                class="col-md-6 card-custom--no-side-margin mt-2"
                :project="initData.project"
                :skillIds="initData.userProject.customProject.skills.map((s) => s.id)"
                :skills="initData.userProject.customProject.skills"
                :skillLevelBit="initData.userProject.customProject.skillLevelBit"
            />
        </div>
    </BasePage>
</template>

<script>
import ApplicationDropdownOpts from "../employerDashboard/ApplicationDropdownOpts";
import BasePage from "../base/BasePage";
import CollapseDiv from "../../components/CollapseDiv";
import EvaluationScoreBadge from "../profile/EvaluationScoreBadge";
import FileDisplay from "../../components/FileDisplay";
import InfoToolTip from "../../components/InfoToolTip";
import ProjectAccordion from "../project/ProjectAccordion";
import formChecker from "../../../utils/form";
import userProjectUtil from "../../../utils/userProject";
import {getAjaxFormData, makeAjaxRequest} from "../../../vueMixins";
import dataUtil from "../../../utils/data";

export default {
    name: "UserProjectPage",
    components: {ApplicationDropdownOpts, BasePage, CollapseDiv, EvaluationScoreBadge, FileDisplay, InfoToolTip, ProjectAccordion},
    computed: {
        canEvaluate() {
            return this.isAdmin || (this.isEmployer  && !this.isSelf(this.initData.userProject.user.id))
        },
        userProject() {
            return this.initData.userProject;
        },
        filesWithThumbnails() {
            return this.userProject.files.filter((f) => f.thumbnail);
        },
        filesWithoutThumbnails() {
            return this.userProject.files.filter((f) => !f.thumbnail);
        }
    },
    data() {
        return {
            hasEvaluated: false,
            isAddEvaluation: false,
            isHardRefresh: true
        }
    },
    methods: {
        getApplicationStatus: dataUtil.getApplicationStatus,
        getBadgeColor: userProjectUtil.getBadgeColor,
        getEvaluationScore: userProjectUtil.getEvaluationScore,
        isEmptyString: formChecker.isEmptyWysiwyg,
        isEvaluatorSelf(evalItem) {
            return evalItem.evaluator.id === this.globalData.uproveUser.id;
        },
        getEvaluatorLabel(evalItem) {
            const evaluator = evalItem.evaluator;
            const evaluatorName = (this.isEvaluatorSelf(evalItem)) ? 'you' : `${evaluator.firstName} ${evaluator.lastName}`;
            return `Evaluation completed by ${evaluatorName}`;
        },
        getEvaluationCriterion(criterionId) {
            return this.initData.userProject.evaluationCriteria.find((ec) => ec.id === criterionId);
        },
        saveEvaluation() {
            const data = {
                userProjectId: this.userProject.id,
                evaluatorId: this.globalData.uproveUser.id,
                evaluationCriteria: (this.hasEvaluated) ? this.initData.userProject.evaluations[this.globalData.uproveUser.id] : this.initData.userProject.evaluationCriteria
            };
            makeAjaxRequest(`${this.apiUrl}user-project-evaluation/`, {
                method: 'PUT',
                data: getAjaxFormData(data),
                success: this.onSaveSuccessFn('PUT'),
                error: this.onSaveFailure
            });
        }
    },
    mounted() {
        this.hasEvaluated = this.globalData.uproveUser.id in (this.initData.userProject.evaluations || {});
    }
}
</script>