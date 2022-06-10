<template>
    <div class="collapse-card card-custom p-0">
        <div class="ps-3 pe-3">
            <h5 class="-skew-top-left me-2">
                <span class="badge -color-darkblue">{{project.role}}</span>
            </h5>
            <h5>
                {{project.title}}
                <slot name="headerAppend"></slot>
            </h5>
            <slot name="afterHeader"></slot>
            <div v-html="project.description" class="mb-2"></div>
        </div>
        <CollapseDiv :elId="getNewElUid()">
            <template v-slot:header>
                Project brief
            </template>
            <div v-html="project.background"></div>
            <div v-if="project.isLimited">
                <a href="/sign-up/">Get started to see the full project brief</a>
            </div>
        </CollapseDiv>
        <CollapseDiv v-if="isLoggedIn" :elId="getNewElUid()">
            <template v-slot:header>
                Instructions
            </template>
            <div class="pb-2">
                <div v-html="project.instructions"></div>
                <ul v-if="skillInstructions.length" class="pb-2">
                    <li v-for="i in skillInstructions">{{i}}</li>
                </ul>
            </div>
        </CollapseDiv>
        <CollapseDiv
            v-if="isLoggedIn && isEmployer && project.evaluationCriteria"
            :elId="getNewElUid()"
            :isClosed="true"
            class="mb-2"
        >
            <template v-slot:header>
                Project evaluation guide <InfoToolTip :elId="getNewElUid()" :content="TOOLTIPS.employerProjectEvaluationGuide"/>
            </template>
            <ul>
                <li v-for="criterion in project.evaluationCriteria">{{criterion.criterion}}</li>
            </ul>
        </CollapseDiv>
        <CollapseDiv v-if="project?.files?.length">
            <template v-slot:header>
                Files
            </template>
            <div v-for="file in project.files">
                <FileDisplay :file="file" :isIncludeDescription="true" :isIncludeSkillLevels="true"/>
            </div>
        </CollapseDiv>
    </div>
</template>

<script>
import CollapseDiv from "../../components/CollapseDiv";
import FileDisplay from "../../components/FileDisplay";
import InfoToolTip from "../../components/InfoToolTip";

export default {
    name: "ProjectAccordion",
    props: ['project', 'skillIds', 'skills'],
    components: {
        CollapseDiv, FileDisplay, InfoToolTip
    },
    computed: {
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