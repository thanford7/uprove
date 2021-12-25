<template>
    <div class="container-lg">
        <BannerAlert/>
        <div class="row mt-3 mb-3" :class="(isMobile) ? 'mobile-top' : ''">
            <div class="col-md-9">
                <h1>{{this.initData.project.title}} <span class="badge -color-darkblue">{{this.initData.project.function}}</span></h1>
                <div v-html="this.initData.project.description" class="-border-bottom--light mb-2"></div>
                <h3>Project brief</h3>
                <div v-html="this.initData.project.background" class="-border-bottom--light mb-2"></div>
                <template v-if="isLoggedIn">
                    <h3>Instructions</h3>
                    <template v-if="formData.skillLevelBit">
                        <div v-html="projectInstructions" class="-border-bottom--light mb-2"></div>
                    </template>
                    <div v-else class="-sub-text -border-bottom--light mb-2">Select skill level to view instructions</div>
                </template>
                <div v-if="this.initData.project.files.length">
                    <h3>Files</h3>
                    <div v-for="file in this.initData.project.files">
                        <FileDisplay :file="file" :isIncludeDescription="true" :isIncludeSkillLevels="true"/>
                    </div>
                </div>
            </div>
            <div class="col-md-3 sidebar mb-3" :class="(isMobile) ? 'mobile-side-margin' : ''">
                <div v-if="this.initData.project.isLimited">
                    <div class="-text-center">
                        Want to view the full project brief and files?
                    </div>
                    <div>
                        <span class="text-label text-label-sm">Employers</span>
                        <button type="button" class="btn btn-sm btn-primary w-100" @click="eventBus.emit('open:employerRequestInfoModal')">
                            Request demo
                        </button>
                    </div>
                    <div>
                        <span class="text-label text-label-sm">Job seekers</span>
                        <button type="button" class="btn btn-sm btn-primary w-100" @click="eventBus.emit('open:candidateRequestAccountModal')">
                            Request account
                        </button>
                    </div>
                </div>
                <div v-else>
                    <h4>Customize project</h4>
                    <template v-if="isEmployer">
                        <InputSelectize
                            ref="employerJobs"
                            elId="employerJobs"
                            placeholder="Job positions" :cfg="employerJobsCfg" @selected="formData.jobIds = $event"
                        />
                    </template>
                    <InputSelectize
                        ref="projectSkillLevel"
                        elId="projectSkillLevel"
                        :isParseAsBits="true"
                        placeholder="Skill level" :cfg="projectSkillLevelCfg" @selected="formData.skillLevelBit = $event"
                    />
                    <InputSelectize
                        ref="projectSkills"
                        elId="projectSkills"
                        :isParseAsInt="true"
                        placeholder="Project skills" :cfg="projectSkillsCfg" @selected="formData.skillIds = $event"
                    />
                    <template v-if="isEmployer">
                        <button @click="readAndSubmitForm" type="button" class="btn btn-primary w-100">Link project to {{pluralize('job position', (formData.jobIds || []).length)}}</button>
                    </template>
                </div>
            </div>
        </div>
        <EmployerRequestInfoModal/>
        <CandidateRequestAccountModal/>
    </div>
</template>

<script>
import {severity} from "../../../vueMixins";
import BannerAlert from "../../components/BannerAlert";
import CandidateRequestAccountModal from "../../modals/CandidateRequestAccountModal";
import dataUtil from "../../../utils/data";
import EmployerRequestInfoModal from "../../modals/EmployerRequestInfoModal";
import FileDisplay from "../../components/FileDisplay";
import InputSelectize from "../../inputs/InputSelectize";

export default {
    name: "ProjectPage.vue",
    components: {BannerAlert, CandidateRequestAccountModal, EmployerRequestInfoModal, FileDisplay, InputSelectize},
    data() {
        return {
            crudUrl: null,  // Set on mounted
            isUpdateData: true,
            initDataKey: 'jobs',
            requiredFields: {
                skillLevelBit: null,
            }
        }
    },
    computed: {
        employerJobsCfg() {
            return {
                plugins: ['remove_button'],
                maxItems: null,
                options: dataUtil.sortBy(this.initData.jobs.map((j) => ({value: j.id, text: j.jobTitle})), 'text')
            };
        },
        projectSkillsCfg() {
            return {
                plugins: ['remove_button'],
                maxItems: null,
                options: dataUtil.sortBy(this.initData.project.skills.map((s) => ({value: s.id, text: s.skillName})), 'text')
            };
        },
        projectSkillLevelCfg() {
            const options = dataUtil.getSkillLevelNumbersFromBits(this.initData.project.skillLevelBits, this.globalData.SKILL_LEVEL).map((sBit) => {
                return {
                    value: sBit,
                    text: this.globalData.SKILL_LEVEL[sBit]
                };
            });
            return {
                maxItems: 1,
                options
            }
        },
        projectInstructions() {
            const instructions = this.initData.project.instructions.find((i) => i.skillLevelBit & this.formData.skillLevelBit)
            return (instructions) ? instructions.instructions : '';
        }
    },
    methods: {
        getSuccessMessage() {
            return 'Successfully linked project to jobs'
        },
        getFailureMessage(errorThrown) {
            return `Failed to link project to jobs: ${errorThrown}`
        },
        isGoodFormFields(formData) {
            if(!formData.jobIds || !formData.jobIds.length) {
                this.addPopover($(this.$refs['employerJobs'].targetEl), {content: 'At least one job is required', severity: severity.WARN, isOnce: true});
                return false;
            }
            if(!formData.skillIds || !formData.skillIds.length) {
                this.addPopover($(this.$refs['projectSkills'].targetEl), {content: 'At least one skill is required', severity: severity.WARN, isOnce: true});
                return false;
            }
            return true;
        }
    },
    mounted() {
        if (this.isEmployer) {
            this.requiredFields.skillLevelBit = this.$refs['projectSkillLevel'].targetEl;
        }
        this.crudUrl = `job-project-link/${this.initData.project.id}/`;
        this.eventBus.on('ajaxSuccess', () => {
            this.clearSelectizeElements()
        });
    }
}
</script>