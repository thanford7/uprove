<template>
    <div v-if="!isLoading" class="collapse-card card-custom card-custom--no-top-margin">
        <slot name="top"></slot>
        <CollapseDiv :elId="getNewElUid()" class="-border-bottom--light" :isClosed="!isCompanyDescriptionOpen">
            <template v-slot:header>Company Profile</template>
            <div v-html="employer.description"></div>
        </CollapseDiv>
        <CollapseDiv :elId="getNewElUid()" class="-border-bottom--light" :isClosed="!isJobDescriptionOpen">
            <template v-slot:header>Job Description</template>
            <div class="job-description" v-html="job.jobDescription"></div>
        </CollapseDiv>
        <template v-if="!isHideProjects" v-for="(ap, idx) in job.allowedProjects">
            <CollapseDiv
                :ref="`accordionItem-${ap.id}`"
                :elId="getNewElUid()"
                class="-border-bottom--light"
            >
                <template v-slot:header>
                    Project Option {{idx + 1}}: {{getProject(ap).title}}
                </template>
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
            </CollapseDiv>
        </template>
        <slot name="bottom"></slot>
    </div>
</template>

<script>
import CollapseDiv from "../../components/CollapseDiv";
import FileDisplay from "../../components/FileDisplay";

export default {
    name: "JobPosting",
    components: {CollapseDiv, FileDisplay},
    props: ['employer', 'job', 'customProjectId', 'isJobDescriptionOpen', 'isCompanyDescriptionOpen', 'isHideProjects'],
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
            return initData.projects[customProject.projectId];
        },
        getProjectInstructions(customProject) {
            const project = this.getProject(customProject);
            return project.instructions;
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
            if (!project) {
                return [];
            }
            return project.files;
        },
    }
}
</script>