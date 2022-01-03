<template>
    <div class="container-lg">

        <div class="row mt-3 mb-3">
            <div class="align-items-center" style="display: flex">
                <img v-if="initData.employer.logo" :src="initData.employer.logo" alt="" class="employer-logo">
                <h2 v-else style="display: inline-block; margin-bottom: 0">{{initData.employer.companyName}}</h2>
                <h2 style="display: inline-block; margin-bottom: 0">{{initData.job.jobTitle}} position</h2>
            </div>
        </div>
        <div class="row mb-3 justify-content-center" :class="(isMobile) ? 'mobile-top' : ''">
            <div :id="accordionElId" class="col-md-9 accordion">
                <AccordionItem :accordionElId="accordionElId" :elId="getNewElUid()">
                    <template v-slot:header>
                        Company Profile
                    </template>
                    <template v-slot:body>
                        <div v-html="initData.employer.description"></div>
                    </template>
                </AccordionItem>
                <AccordionItem :accordionElId="accordionElId" :elId="getNewElUid()">
                    <template v-slot:header>
                        Job Description
                    </template>
                    <template v-slot:body>
                        <span v-html="initData.job.jobDescription"></span>
                    </template>
                </AccordionItem>
                <template v-for="(ap, idx) in initData.job.allowedProjects">
                    <AccordionItem :ref="`accordionItem-${ap.id}`" :accordionElId="accordionElId" :elId="getNewElUid()" :isOpen="true">
                        <template v-slot:header>
                            Project Option {{idx + 1}}: {{getProject(ap).title}}
                        </template>
                        <template v-slot:body>
                            <h5 class="-text-bold">Description</h5>
                            <p v-html="getProject(ap).description" class="-border-bottom--light"></p>
                            <h5 class="-text-bold">Background</h5>
                            <p v-html="getProject(ap).background" class="-border-bottom--light"></p>
                            <div class="mb-3" :class="(getProjectFiles(ap).length) ? '-border-bottom--light' : ''">
                                <h5 class="-text-bold">Instructions</h5>
                                <p v-html="getProjectInstructions(ap)"></p>
                                <ul v-if="getProjectSkillInstructions(ap)" class="pb-2">
                                    <li v-for="i in getProjectSkillInstructions(ap)">{{i}}</li>
                                </ul>
                            </div>
                            <template v-if="getProjectFiles(ap).length">
                                <h5 class="-text-bold">Files</h5>
                                <FileDisplay v-for="file in getProjectFiles(ap)" :file="file"/>
                            </template>
                        </template>
                    </AccordionItem>
                </template>
            </div>
            <div class="col-md-3 sidebar mb-3" :class="(isMobile) ? 'mobile-side-margin' : ''">
                <h5 class="-text-bold">Applicant instructions</h5>
                <ol class="-border-bottom--light mb-3 pb-3">
                    <li v-if="!isLoggedIn" id="loginInstruction">
                        <a href="#" @click="eventBus.emit('open:candidateRequestAccountModal')">Create an account</a>
                        or
                        <a href="#" @click="eventBus.emit('open:signInModal')">sign in</a>
                    </li>
                    <li v-if="initData.job.allowedProjects.length > 1">
                        Select a project
                        <InputSelectize
                            ref="allowedProjects"
                            elId="allowedProjects"
                            placeholder="Required" :cfg="allowedProjectsCfg" @selected="selectAndSetProject"
                        />
                    </li>
                    <li>
                        Read project description, background, and instructions
                    </li>
                    <li v-if="hasFiles">
                        Download project files
                    </li>
                    <li>
                        <button
                            @click="saveChange" type="button" class="btn btn-primary w-75"
                            :disabled="(isLoggedIn) ? null : true"
                            :title="(isLoggedIn) ? null : 'Must be logged in to save project'"
                        >
                            Save project to your profile
                        </button>
                    </li>
                    <li>
                        Upload your final project files and submit your final project to {{initData.employer.companyName}}
                        from your home page
                    </li>
                </ol>
                <div class="-sub-text">Need help or have questions about the project?</div>
                <div class="-sub-text"><a href="#">Submit question</a></div>
            </div>
        </div>
        <CandidateRequestAccountModal/>
    </div>
</template>

<script>
import AccordionItem from "../../components/AccordionItem";
import BannerAlert from "../../components/BannerAlert";
import CandidateRequestAccountModal from "../../modals/CandidateRequestAccountModal";
import FileDisplay from "../../components/FileDisplay";
import InputSelectize from "../../inputs/InputSelectize";

export default {
    name: "JobPostingPage.vue",
    components: {AccordionItem, BannerAlert, CandidateRequestAccountModal, FileDisplay, InputSelectize},
    data() {
        return {
            accordionElId: `accordion-${this.getNewElUid()}`,
            crudUrl: 'user-job-application/',
            requiredFields: {
                customProjectId: null,
                userId: '#loginInstruction'
            },
            pageRedirect: 'candidateDashboard/'
        }
    },
    computed: {
        allowedProjectsCfg() {
            return {
                maxItems: 1,
                options: this.initData.job.allowedProjects.map((ap) => ({value: ap.id, text: ap.projectTitle}))
            }
        },
        hasFiles() {
            const customProjects = this.initData.job.allowedProjects.filter((cp) => !this.formData.customProjectId || cp.id === this.formData.customProjectId);
            return customProjects.reduce((hasFiles, ap) => {
                return hasFiles || this.getProjectFiles(ap).length;
            }, false);
        }
    },
    methods: {
        getProject(customProject) {
            return this.initData.projects[customProject.projectId];
        },
        getProjectInstructions(customProject) {
            const project = this.getProject(customProject);
            return project.instructions.find((i) => i.skillLevelBit === customProject.skillLevelBit).instructions
        },
        getProjectSkillInstructions(customProject) {
            return customProject.skills.reduce((instructions, skill) => {
                if (skill.instruction) {
                    instructions.push(skill.instruction);
                }
                return instructions;
            }, []);
        },
        getProjectFiles(customProject) {
            const project = this.getProject(customProject);
            return project.files.filter((f) => f.skillLevelBits & customProject.skillLevelBit)
        },
        processFormData() {
            return Object.assign(this.readForm(), {
                'userId': this.globalData.uproveUser.id,
                'employerJobId': this.initData.job.id
            })
        },
        getAjaxCfgOverride() {
            return {method: 'POST'}
        },
        selectAndSetProject(customProjectId) {
            this.formData.customProjectId = customProjectId;
            if (!customProjectId) {
                return;
            }
            const accordionItem = this.$refs[`accordionItem-${customProjectId}`];
            $(`#${accordionItem.accordionElId}`).find('.accordion-header').each((idx, el) => {
                const isShown = $(el).prop('id') === accordionItem.headerElId;
                const accordionButton = $(el).find('button.accordion-button');
                if (isShown === accordionButton.hasClass('collapsed')) {
                    accordionButton.click();
                }
            });
        }
    },
    mounted() {
        if (this.initData.job.allowedProjects.length > 1) {
            this.requiredFields.customProjectId = this.$refs.allowedProjects.targetEl;
        } else if (this.initData.job.allowedProjects.length) {
            this.formData.customProjectId = this.initData.job.allowedProjects[0].id;
        }
    }
}
</script>