<template>
    <div class="container-lg">
        <div class="row mt-3 mb-3">
            <div class="align-items-center" style="display: flex">
                <img v-if="initData.employer.logo" :src="initData.employer.logo" alt="" class="employer-logo">
                <h2 v-else style="display: inline-block; margin-bottom: 0">{{initData.employer.companyName}}</h2>
                <h2 style="display: inline-block; margin-bottom: 0">{{initData.job.jobTitle}} position</h2>
            </div>
        </div>
        <div class="row mb-3 justify-content-center">
            <div :id="accordionElId" class="col-md-9 accordion">
                <AccordionItem :accordionElId="accordionElId" :elId="getNewElUid()">
                    <template v-slot:header>
                        Company Profile
                    </template>
                    <template v-slot:body>
                        Lorem ipsum
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
                    <AccordionItem :accordionElId="accordionElId" :elId="getNewElUid()" :isOpen="true">
                        <template v-slot:header>
                            Project Option {{idx + 1}}: {{getProject(ap).title}}
                        </template>
                        <template v-slot:body>
                            <h5 class="-text-bold">Description</h5>
                            <p v-html="getProject(ap).description" class="-border-bottom--light"></p>
                            <h5 class="-text-bold">Background</h5>
                            <p v-html="getProject(ap).background" class="-border-bottom--light"></p>
                            <h5 class="-text-bold">Instructions</h5>
                            <p v-html="getProjectInstructions(ap)" :class="(getProjectFiles(ap).length) ? '-border-bottom--light' : ''"></p>
                            <template v-if="getProjectFiles(ap).length">
                                <h5 class="-text-bold">Files</h5>
                                <FileDisplay v-for="file in getProjectFiles(ap)" :file="file"/>
                            </template>
                        </template>
                    </AccordionItem>
                </template>
            </div>
        </div>
    </div>
</template>

<script>
import AccordionItem from "../../components/AccordionItem";
import FileDisplay from "../../components/FileDisplay";

export default {
    name: "JobPostingPage.vue",
    components: {AccordionItem, FileDisplay},
    data() {
        return {
            accordionElId: `accordion-${this.getNewElUid()}`
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
        getProjectFiles(customProject) {
            const project = this.getProject(customProject);
            return project.files.filter((f) => f.skillLevelBits & customProject.skillLevelBit)
        }
    }
}
</script>