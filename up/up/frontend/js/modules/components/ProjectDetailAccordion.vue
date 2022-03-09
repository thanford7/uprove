<template>
    <div id="projectInfo" class="accordion mb-3 mt-3">
        <AccordionItem accordionElId="projectInfo" :elId="getNewElUid()" :isOpen="false" :isAllowMultipleOpen="true">
            <template v-slot:header>
                Project description
            </template>
            <template v-slot:body>
                <div v-html="userProject.customProject.projectDescription"></div>
            </template>
        </AccordionItem>
        <AccordionItem accordionElId="projectInfo" :elId="getNewElUid()" :isOpen="false" :isAllowMultipleOpen="true">
            <template v-slot:header>
                Project background
            </template>
            <template v-slot:body>
                <div v-html="userProject.customProject.projectBackground"></div>
            </template>
        </AccordionItem>
        <AccordionItem
            v-if="userProject.customProject.projectInstructions"
            accordionElId="projectInfo"
            :elId="getNewElUid()"
            :isOpen="false"
            :isAllowMultipleOpen="true"
        >
            <template v-slot:header>
                Project instructions
            </template>
            <template v-slot:body>
                <div v-html="projectInstructionsWithSkills"></div>
            </template>
        </AccordionItem>
    </div>
</template>

<script>
import AccordionItem from "./AccordionItem";
export default {
    name: "ProjectDetailAccordion",
    props: ['userProject'],
    computed: {
        projectInstructionsWithSkills() {
            return [
                this.userProject.customProject.projectInstructions,
                ...this.userProject.customProject.skills.map((s) => s.instruction)
            ].join(' ')
        }
    },
    components: {AccordionItem}
}
</script>