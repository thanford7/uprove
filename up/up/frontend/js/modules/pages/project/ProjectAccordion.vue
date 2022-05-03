<template>
    <div class="card-custom">
        <h5 class="-skew-top-left me-2">
            <span class="badge -color-darkblue">{{project.role}}</span>
        </h5>
        <ProjectJobs v-if="project.jobs" :jobs="project.jobs" class="mt-3 mb-2"/>
        <h5>{{project.title}}</h5>
        <div v-html="project.description" class="-border-bottom--light mb-2"></div>
        <CollapseDiv :elId="getNewElUid()" :class="(project.isLimited) ? '' : '-border-bottom--light mb-2'">
            <template v-slot:header>
                <h5>Project brief</h5>
            </template>
            <div v-html="project.background"></div>
            <div v-if="project.isLimited">
                <a href="/sign-up/">Get started to see the full project brief</a>
            </div>
        </CollapseDiv>
        <CollapseDiv v-if="isLoggedIn" :elId="getNewElUid()" class="-border-bottom--light mb-2">
            <template v-slot:header>
                <h5>Instructions</h5>
            </template>
            <div v-if="skillLevelBit" class="pb-2">
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
                <h5>Project evaluation guide <InfoToolTip :elId="getNewElUid()" :content="TOOLTIPS.employerProjectEvaluationGuide"/></h5>
            </template>
            <ul>
                <li v-for="criterion in evaluationCriteria">{{criterion.criterion}}</li>
            </ul>
        </CollapseDiv>
        <CollapseDiv v-if="projectFiles.length">
            <template v-slot:header>
                <h5>Files</h5>
            </template>
            <div v-for="file in projectFiles">
                <FileDisplay :file="file" :isIncludeDescription="true" :isIncludeSkillLevels="true"/>
            </div>
        </CollapseDiv>
    </div>
</template>

<script>
import CollapseDiv from "../../components/CollapseDiv";
import FileDisplay from "../../components/FileDisplay";
import InfoToolTip from "../../components/InfoToolTip";
import ProjectJobs from "../projects/ProjectJobs";

export default {
    name: "ProjectAccordion",
    props: ['project', 'skillLevelBit', 'skillIds', 'skills'],
    components: {
        CollapseDiv, FileDisplay, InfoToolTip, ProjectJobs
    },
    computed: {
        evaluationCriteria() {
            return this.project.evaluationCriteria.filter((ec) => {
                return !ec.skillLevelBits || !this.skillLevelBit || ec.skillLevelBits & this.skillLevelBit;
            });
        },
        projectFiles() {
            return this.project.files.filter((file) => !this.skillLevelBit || file.skillLevelBits & this.skillLevelBit);
        },
        projectInstructions() {
            const instructions = this.project.instructions.find((i) => i.skillLevelBit & this.skillLevelBit)
            return (instructions) ? instructions.instructions : '';
        },
        skillInstructions() {
            if (!this.skillIds) {
                return [];
            }
            return this.skillIds.reduce((instructions, sId) => {
                const skill = this.skills.find((skill) => skill.id === sId);
                if (skill.instruction) {
                    instructions.push(skill.instruction);
                }
                return instructions;
            }, []);
        }
    }
}
</script>