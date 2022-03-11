<template>
    <BasePage>
        <div class="row" :class="(isMobile) ? 'mobile-top' : ''">
            <div class="col-md-8 card-custom">
                <h1>{{initData.project.title}} <span class="badge -color-darkblue">{{initData.project.role}}</span></h1>
                <div v-html="initData.project.description" class="-border-bottom--light mb-2"></div>
                <CollapseDiv :elId="getNewElUid()" :class="(initData.project.isLimited) ? '' : '-border-bottom--light mb-2'">
                    <template v-slot:header>
                        <h3>Project brief</h3>
                    </template>
                    <div v-html="initData.project.background"></div>
                    <div v-if="initData.project.isLimited">
                        <a href="/sign-up/">Get started to see the full project brief</a>
                    </div>
                </CollapseDiv>
                <CollapseDiv v-if="isLoggedIn" :elId="getNewElUid()" class="-border-bottom--light mb-2">
                    <template v-slot:header>
                        <h3>Instructions</h3>
                    </template>
                    <div v-if="formData.skillLevelBit" class="pb-2">
                        <div v-html="projectInstructions"></div>
                        <ul v-if="skillInstructions.length" class="pb-2">
                            <li v-for="i in skillInstructions">{{i}}</li>
                        </ul>
                    </div>
                    <div v-else class="-sub-text pb-2">Select career level to view instructions</div>
                </CollapseDiv>
                <CollapseDiv
                    v-if="isLoggedIn && isEmployer && evaluationCriteria"
                    :elId="getNewElUid()"
                    :isClosed="true"
                    class="-border-bottom--light mb-2"
                >
                    <template v-slot:header>
                        <h3>Project evaluation guide <InfoToolTip :elId="getNewElUid()" :content="TOOLTIPS.employerProjectEvaluationGuide"/></h3>
                    </template>
                    <ul>
                        <li v-for="criterion in evaluationCriteria">{{criterion.criterion}}</li>
                    </ul>
                </CollapseDiv>
                <CollapseDiv v-if="projectFiles.length">
                    <template v-slot:header>
                        <h3>Files</h3>
                    </template>
                    <div v-for="file in projectFiles">
                        <FileDisplay :file="file" :isIncludeDescription="true" :isIncludeSkillLevels="true"/>
                    </div>
                </CollapseDiv>
            </div>
            <div v-if="this.initData.project.isLimited" class="col-md-3 sidebar mb-3" :class="(isMobile) ? 'mobile-side-margin' : ''">
                <div class="-text-center">
                    Want to view the full project brief and files?
                </div>
                <div>
                    <button type="button" class="btn btn-sm btn-primary w-100" @click="redirectUrl('/sign-up/')">
                        Get started
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
                            <SkillsSelectize
                                ref="skills"
                                :skills="initData.project.skills"
                                :cfg="{isMulti: true, projectId: initData.project.id, placeholder: 'Skills'}"
                                @selected="formData.skillIds = $event"
                            />
                            <template v-if="isEmployer">
                                <button @click="readAndSubmitForm" type="button" class="btn btn-primary w-100">Link project to {{pluralize('job position', (formData.jobIds || []).length)}}</button>
                            </template>
                            <template v-else>
                                <button @click="readAndSubmitForm" type="button" class="btn btn-primary w-100">Save project to dashboard</button>
                            </template>
                        </template>
                    </AccordionItem>
                    <AccordionItem
                        v-if="existingProjects && Object.values(existingProjects).length"
                        :accordionElId="accordionElId" :elId="getNewElUid()" :isOpen="!isMobile" :isAllowMultipleOpen="true"
                    >
                        <template v-slot:header>
                            <template v-if="isEmployer">
                                <span>Linked job positions&nbsp;</span><InfoToolTip :elId="getNewElUid()" content="These are projects that have already been linked to one or more job positions"/>
                            </template>
                            <template v-else>
                                <span>Linked projects&nbsp;</span><InfoToolTip :elId="getNewElUid()" content="These are projects that you have already added to your profile"/>
                            </template>
                        </template>
                        <template v-slot:body>
                            <div v-for="(proj, projId, idx) in existingProjects" class="mb-2 -hover-highlight-border" :class="(!isLastItem(idx, existingProjects)) ? '-border-bottom--light' : ''">
                                <p><b>Project #{{idx + 1}}</b></p>
                                <div class="mb-1 pb-1">
                                    <div class="text-label text-label-sm">CAREER LEVEL</div>
                                    <BadgesSkillLevels :skillLevels="proj.customProject.skillLevels"/>
                                </div>
                                <div class="mb-1 pb-1">
                                    <div class="text-label text-label-sm">SKILLS</div>
                                    <BadgesSkills :skills="proj.customProject.skills"/>
                                </div>
                                <template v-if="isEmployer">
                                    <div class="text-label text-label-sm">JOB POSITIONS</div>
                                    <table>
                                        <tbody>
                                            <tr v-for="job in proj.jobs">
                                                <td><i class="fas fa-trash -color-red-text" title="Unlink job" @click="unlinkJob(proj.customProject, job)"></i>&nbsp;</td>
                                                <td>{{job.jobTitle}}</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </template>
                            </div>
                        </template>
                    </AccordionItem>
                </div>
            </template>
        </div>
    </BasePage>
    <EditUserModal/>
    <EmployerRequestInfoModal/>
</template>

<script>
import {SEVERITY} from "../../../globalData";
import AccordionItem from "../../components/AccordionItem";
import BadgesSkillLevels from "../../components/BadgesSkillLevels";
import BadgesSkills from "../../components/BadgesSkills";
import BannerAlert from "../../components/BannerAlert";
import CollapseDiv from "../../components/CollapseDiv";
import dataUtil from "../../../utils/data";
import EditUserModal from "../../modals/EditUserModal";
import EmployerRequestInfoModal from "../../modals/EmployerRequestInfoModal";
import FileDisplay from "../../components/FileDisplay";
import InfoToolTip from "../../components/InfoToolTip";
import InputSelectize from "../../inputs/InputSelectize";
import skillLevelSelectize from "../../selectizeCfgs/skillLevels";
import skillSelectize from "../../selectizeCfgs/skill";
import SkillsSelectize from "../../inputs/SkillsSelectize";
import BasePage from "../BasePage";

export default {
    name: "ProjectPage.vue",
    components: {
        BasePage,
        AccordionItem, BannerAlert, BadgesSkillLevels, BadgesSkills, CollapseDiv, EditUserModal,
        EmployerRequestInfoModal, FileDisplay, InfoToolTip, InputSelectize, SkillsSelectize
    },
    data() {
        return {
            crudUrl: null,  // Set on mounted
            pageRedirect: null, // Set on mounted
            isUpdateData: true,
            initDataKey: null,
            requiredFields: {
                skillLevelBit: null,
            },
            accordionElId: `accordion-${this.getNewElUid()}`,
        }
    },
    computed: {
        existingProjects() {
            if (!this.isEmployer) {
                return this.initData.userProjects.reduce((projects, p) => {
                    // Only display user projects related to the current project
                    if (this.initData.project.id === p.customProject.projectId) {
                        projects[p.id] = p;
                    }
                    return projects;
                }, {});
            }
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
        evaluationCriteria() {
            return this.initData.project.evaluationCriteria.filter((ec) => {
                return !ec.skillLevelBits || !this.formData.skillLevelBit || ec.skillLevelBits & this.formData.skillLevelBit;
            });
        },
        employerJobsCfg() {
            return {
                plugins: ['remove_button'],
                maxItems: null,
                options: dataUtil.sortBy(this.initData.jobs.map((j) => ({value: j.id, text: j.jobTitle})), 'text')
            };
        },
        projectSkillLevelCfg() {
            const options = this.getSkillLevelNumbersFromBits(this.initData.project.skillLevelBits).map((sBit) => {
                return {
                    value: sBit,
                    text: this.globalData.SKILL_LEVEL[sBit].title
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
        skillInstructions() {
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
            return (!this.isEmployer) ? 'Added project to profile' : 'Successfully linked project to jobs';
        },
        getFailureMessagePrepend() {
            return (!this.isEmployer) ? 'Failed to add project: ' : 'Failed to link project to jobs: ';
        },
        isGoodFormFields(formData) {
            if(this.isEmployer && (!formData.jobIds || !formData.jobIds.length)) {
                this.addPopover($(this.$refs.employerJobs.targetEl), {content: 'At least one job is required', severity: SEVERITY.WARN, isOnce: true});
                return false;
            }
            if(!formData.skillIds || !formData.skillIds.length) {
                this.addPopover($(this.$refs.skills.targetEl), {content: 'At least one skill is required', severity: SEVERITY.WARN, isOnce: true});
                return false;
            }
            return true;
        },
        processFormData() {
            const formData = this.readForm();
            formData.userId = this.globalData.uproveUser.id;
            formData.projectId = this.initData.project.id;

            return formData;
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
        afterUpdateInitData() {
            if (this.isEmployer) {
                this.setJobSkillLevels(this.initData.jobs);
            } else {
                this.setUserProjectSkillLevels(this.initData.userProjects);
            }
        },
        setJobSkillLevels(jobs) {
            jobs.forEach((j) => { skillLevelSelectize.setSkillLevels(j.allowedProjects,  true); });
        },
        setUserProjectSkillLevels(userProjects) {
            userProjects.forEach((up) => { skillLevelSelectize.setSkillLevels([up.customProject], true); });
        }
    },
    mounted() {
        // Set skill levels from bits
        if (this.initData.jobs) {
            this.setJobSkillLevels(this.initData.jobs);
        }
        if (this.initData.userProjects) {
            this.setUserProjectSkillLevels(this.initData.userProjects);
        }
        if (this.initData.userProjects) {
            skillLevelSelectize.setSkillLevels(this.initData.userProjects, true);
        }

        if (!initData.project.isLimited) {
            this.requiredFields.skillLevelBit = this.$refs.projectSkillLevel.targetEl;
            this.initDataKey = (this.isEmployer) ? 'jobs' : 'userProjects';
            const {skillLevel, skill} = dataUtil.getQueryParams();
            const defaultSkillLevel = (this.projectSkillLevelCfg.options.length === 1) ? this.projectSkillLevelCfg.options[0].value : null;
            this.$refs.skills.setValue(skill || skillSelectize.getDefaultSkills(this.initData.project.skills));
            this.$refs.projectSkillLevel.elSel.setValue(skillLevel || defaultSkillLevel);
        }

        const popoverCfgs = [];
        if (this.isEmployer) {
            this.crudUrl = `job-project-link/${this.initData.project.id}/`;
            if (!this.employerJobsCfg.options.length) {
                popoverCfgs.push({
                    el$: $(this.$refs.employerJobs.targetEl),
                    content: 'You do not have any job positions. Go to your Employer Dashboard to create your first job position.',
                });
            } else {
                popoverCfgs.push({
                    el$: $(this.$refs.employerJobs.targetEl),
                    content: 'Select one or more job positions where candidates can use this project to apply for the job.',
                    clickTarget: this.$refs.employerJobs.targetEl
                });
            }
            if (!this.$refs.projectSkillLevel.elSel.getValue()) {
                popoverCfgs.push({
                    el$: $(this.$refs.projectSkillLevel.targetEl),
                    content: 'Choose your desired career level. The instructions for this project will change based on the selected level.',
                    clickTarget: this.$refs.projectSkillLevel.targetEl,
                    showEvent: {target$: $(this.$refs.employerJobs.targetEl), event: 'blur'}
                });
            }
            popoverCfgs.push({
                el$: $(this.$refs.skills.targetEl),
                content: `These are the recommended skills based on common skills required for a ${this.initData.project.role} role. You can add or remove skills based on the type of role you are hiring for.`,
                showEvent: {target$: $(this.$refs.projectSkillLevel.targetEl), event: 'blur'}
            });
        } else if (this.isCandidate) {
            this.crudUrl = 'user-project/';
            this.pageRedirect = `/candidateDashboard/${this.globalData.uproveUser.id}/`;
            // Only add this info popover if the skill level is unset
            if (!this.$refs.projectSkillLevel.elSel.getValue()) {
                popoverCfgs.push({
                    el$: $(this.$refs.projectSkillLevel.targetEl),
                    content: 'Choose your desired career level to get started.',
                    clickTarget: this.$refs.projectSkillLevel.targetEl
                });
            }
            popoverCfgs.push({
                el$: $(this.$refs.skills.targetEl),
                content: 'These are the recommended skills based on employer interest. Adding skills will allow you to show off more of your talent, but will also increase the time to complete the project.',
                showEvent: (popoverCfgs.length) ? {target$: $(this.$refs.projectSkillLevel.targetEl), event: 'blur'} : null
            });
        }
        this.createPopoverChain(popoverCfgs, {severity: SEVERITY.INFO, isOnce: true});
    }
}
</script>