<template>
    <div class="container-lg">
        <BannerAlert/>
        <div class="row mt-3 mb-3" :class="(isMobile) ? 'mobile-top' : ''">
            <div class="col-md-9">
                <h1>{{initData.project.title}} <span class="badge -color-darkblue">{{initData.project.function}}</span></h1>
                <div v-html="initData.project.description" class="-border-bottom--light mb-2"></div>
                <h3>Project brief</h3>
                <div v-html="initData.project.background" class="-border-bottom--light mb-2"></div>
                <template v-if="isLoggedIn">
                    <h3>Instructions</h3>
                    <template v-if="formData.skillLevelBit">
                        <div class="-border-bottom--light mb-2">
                            <div v-html="projectInstructions"></div>
                            <ul v-if="projectSkillInstructions.length" class="pb-2">
                                <li v-for="i in projectSkillInstructions">{{i}}</li>
                            </ul>
                        </div>
                    </template>
                    <div v-else class="-sub-text -border-bottom--light mb-2">Select career level to view instructions</div>
                </template>
                <div v-if="projectFiles.length">
                    <h3>Files</h3>
                    <div v-for="file in projectFiles">
                        <FileDisplay :file="file" :isIncludeDescription="true" :isIncludeSkillLevels="true"/>
                    </div>
                </div>
            </div>
            <div v-if="this.initData.project.isLimited" class="col-md-3 sidebar mb-3" :class="(isMobile) ? 'mobile-side-margin' : ''">
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
            <template v-else>
                <div :id="accordionElId" class="col-md-3 accordion mb-3" :class="(isMobile) ? 'mobile-side-margin' : ''">
                    <AccordionItem :accordionElId="accordionElId" :elId="getNewElUid()" :isOpen="true" :isAllowMultipleOpen="true">
                        <template v-slot:header>
                            Customize project
                        </template>
                        <template v-slot:body>
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
                                placeholder="Career level" :cfg="projectSkillLevelCfg" @selected="formData.skillLevelBit = $event"
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
                        </template>
                    </AccordionItem>
                    <AccordionItem
                        v-if="existingProjects && Object.values(existingProjects).length"
                        :accordionElId="accordionElId" :elId="getNewElUid()" :isOpen="!isMobile" :isAllowMultipleOpen="true"
                    >
                        <template v-slot:header>
                            Current projects
                        </template>
                        <template v-slot:body>
                            <div v-for="(proj, projId, idx) in existingProjects" class="mb-2 -hover-highlight-border" :class="(!isLastItem(idx, existingProjects)) ? '-border-bottom--light' : ''">
                                <div class="mb-1 pb-1">
                                    <div class="text-label text-label-sm">CAREER LEVEL</div>
                                    <BadgesSkillLevels :skillLevels="proj.customProject.skillLevels"/>
                                </div>
                                <div class="mb-1 pb-1">
                                    <div class="text-label text-label-sm">SKILLS</div>
                                    <BadgesSkills :skills="proj.customProject.skills"/>
                                </div>
                                <div class="text-label text-label-sm">JOB POSITIONS</div>
                                <table>
                                    <tbody>
                                        <tr v-for="job in proj.jobs">
                                            <td><i class="fas fa-trash -color-red-text" title="Unlink job" @click="unlinkJob(proj.customProject, job)"></i>&nbsp;</td>
                                            <td>{{job.jobTitle}}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </template>
                    </AccordionItem>
                </div>
            </template>
        </div>
        <EmployerRequestInfoModal/>
        <CandidateRequestAccountModal/>
    </div>
</template>

<script>
import {severity} from "../../../vueMixins";
import AccordionItem from "../../components/AccordionItem";
import BadgesSkillLevels from "../../components/BadgesSkillLevels";
import BadgesSkills from "../../components/BadgesSkills";
import BannerAlert from "../../components/BannerAlert";
import CandidateRequestAccountModal from "../../modals/CandidateRequestAccountModal";
import dataUtil from "../../../utils/data";
import EmployerRequestInfoModal from "../../modals/EmployerRequestInfoModal";
import FileDisplay from "../../components/FileDisplay";
import InputSelectize from "../../inputs/InputSelectize";

export default {
    name: "ProjectPage.vue",
    components: {
        AccordionItem, BannerAlert, BadgesSkillLevels, BadgesSkills, CandidateRequestAccountModal,
        EmployerRequestInfoModal, FileDisplay, InputSelectize
    },
    data() {
        return {
            crudUrl: null,  // Set on mounted
            isUpdateData: true,
            initDataKey: 'jobs',
            requiredFields: {
                skillLevelBit: null,
            },
            accordionElId: `accordion-${this.getNewElUid()}`,
        }
    },
    computed: {
        existingProjects() {
            return this.initData.jobs.reduce((uniqueProjects, j) => {
                j.allowedProjects.forEach((p) => {
                    if (p.projectId !== this.initData.project.id) {
                        return;
                    }
                    if (!(p.id in uniqueProjects)) {
                        uniqueProjects[p.id] = {customProject: p, jobs: [j]};
                    } else {
                        uniqueProjects[p.id].jobs.push(j);
                    }
                });
                return uniqueProjects;
            }, {});
        },
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
        projectFiles() {
            return this.initData.project.files.filter((file) => !this.formData.skillLevelBit || file.skillLevelBits & this.formData.skillLevelBit);
        },
        projectInstructions() {
            const instructions = this.initData.project.instructions.find((i) => i.skillLevelBit & this.formData.skillLevelBit)
            return (instructions) ? instructions.instructions : '';
        },
        projectSkillInstructions() {
            if (!this.formData.skillIds) {
                return [];
            }
            return this.formData.skillIds.reduce((instructions, sId) => {
                const skill = this.initData.skills.find((skill) => skill.id === sId);
                if (skill.instruction) {
                    instructions.push(skill.instruction);
                }
                return instructions;
            }, [])
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
        },
        isLastItem(idx, targetObject) {
            return idx === Object.values(targetObject).length - 1;
        },
        unlinkJob(customProject, job) {
            const ajaxData = this.getAjaxFormData({
                jobId: job.id,
                skillLevelBit: customProject.skillLevelBit,
                skillIds: customProject.skillIds
            })

            this.submitAjaxRequest(ajaxData, {
                method: 'DELETE',
                success: () => {
                    job.allowedProjects = job.allowedProjects.filter((ap) => ap.id !== customProject.id);
                }
            });
        },
        getDeleteConfirmationMessage() {
            return `Are you sure you want to unlink this job from the custom project? Job applicants that have` +
            ` already started the project will still be able to submit their project, but no new applicants will be` +
            ` able to use it.`
        },
        updateInitDataPost(jobs) {
            this.setJobSkillLevels(jobs);
            this.initData.jobs = jobs;
        },
        setJobSkillLevels(jobs) {
            jobs.forEach((j) => { dataUtil.setSkillLevels(j.allowedProjects, this.globalData, true); });
        }
    },
    mounted() {
        if (this.isEmployer) {
            this.requiredFields.skillLevelBit = this.$refs['projectSkillLevel'].targetEl;
        }

        // Set skill levels from bits
        if (this.initData.jobs) {
            this.setJobSkillLevels(this.initData.jobs);
        }
        if (this.initData.userProjects) {
            dataUtil.setSkillLevels(this.initData.userProjects, this.globalData, true);
        }

        this.crudUrl = `job-project-link/${this.initData.project.id}/`;
        this.eventBus.on('ajaxSuccess', () => {
            this.clearSelectizeElements()
        });

        if (!initData.project.isLimited) {
            const {skillLevel, skill} = dataUtil.getQueryParams();
            this.$refs['projectSkills'].elSel.setValue(skill);
            this.$refs['projectSkillLevel'].elSel.setValue(skillLevel);
        }
    }
}
</script>