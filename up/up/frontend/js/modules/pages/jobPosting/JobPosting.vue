<template>
    <div v-if="!isLoading" :id="accordionElId" class="accordion">
        <slot name="top"></slot>
        <AccordionItem :accordionElId="accordionElId" :elId="getNewElUid()" :isOpen="isCompanyDescriptionOpen">
            <template v-slot:header>
                Company Profile
            </template>
            <template v-slot:body>
                <div v-html="employer.description"></div>
            </template>
        </AccordionItem>
        <AccordionItem :accordionElId="accordionElId" :elId="getNewElUid()" :isOpen="isJobDescriptionOpen">
            <template v-slot:header>
                Job Description
            </template>
            <template v-slot:body>
                <div class="job-description" v-html="job.jobDescription"></div>
            </template>
        </AccordionItem>
        <template v-for="(ap, idx) in job.allowedProjects">
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
                        <ul v-if="getSkillInstructions(ap)" class="pb-2">
                            <li v-for="i in getSkillInstructions(ap)">{{i}}</li>
                        </ul>
                    </div>
                    <template v-if="getProjectFiles(ap).length">
                        <h5 class="-text-bold">Files</h5>
                        <FileDisplay v-for="file in getProjectFiles(ap)" :file="file"/>
                    </template>
                </template>
            </AccordionItem>
        </template>
        <slot name="bottom"></slot>
    </div>
</template>

<script>
import AccordionItem from "../../components/AccordionItem";
import FileDisplay from "../../components/FileDisplay";

export default {
    name: "JobPosting",
    components: {AccordionItem, FileDisplay},
    props: ['employer', 'job', 'customProjectId', 'isJobDescriptionOpen', 'isCompanyDescriptionOpen'],
    data() {
        return {
            accordionElId: this.getNewElUid(),
        }
    },
    computed: {
        hasFiles() {
            const customProjects = this.job.allowedProjects.filter((cp) => !this.customProjectId || cp.id === this.customProjectId);
            return customProjects.reduce((hasFiles, ap) => {
                return hasFiles || this.getProjectFiles(ap).length;
            }, false);
        },
    },
    methods: {
        getProject(customProject) {
            return (this.cData.projects || []).find((p) => p.id === customProject.projectId);
        },
        getProjectInstructions(customProject) {
            const project = this.getProject(customProject);
            return project.instructions.find((i) => i.skillLevelBit === customProject.skillLevelBit).instructions
        },
        getSkillInstructions(customProject) {
            return customProject.skills.reduce((instructions, skill) => {
                if (skill.instruction) {
                    instructions.push(skill.instruction);
                }
                return instructions;
            }, []);
        },
        getProjectFiles(customProject) {
            const project = this.getProject(customProject);
            return (project) ? project.files.filter((f) => f.skillLevelBits & customProject.skillLevelBit) : [];
        },
    },
    async created() {
        await this.loadData([{route: `project?employerId=${this.employer.id}`, dataKey: 'projects'}]);
    }
}
</script>