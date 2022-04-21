<template>
    <div v-if="project">
        <label class="form-label">
            Customize {{project.title}} Project
            <a href="#" @click="openCustomProject(customProject, $event)"><i class="fas fa-external-link-alt"></i> View customized project</a>
        </label>
        <InputSelectize
            :ref="getSkillLevelRef()"
            :elId="getNewElUid()"
            :items="[customProject.skillLevelBit]"
            :isParseAsBits="true"
            placeholder="Skill level (required)"
            :cfg="getProjectSkillLevelsCfg(customProject)"
            @selected="customProject.skillLevelBit = $event"
        />
        <SkillsSelectize
            :ref="`modalJobCustomProject-skills-${customProject.id}`"
            :items="getDefaultSkills(customProject)"
            :skills="project.skills"
            :cfg="{isMulti: true, projectId: project.id, isIncludeDetails: true, placeholder: 'Skills (required)'}"
            @selected="customProject.skillIds = $event"
        />
    </div>
</template>

<script>
import customProjectUtil from "../../utils/customProject";
import InputSelectize from "./InputSelectize";
import SkillsSelectize from "./SkillsSelectize";
import skillSelectize from "../selectizeCfgs/skill";

export default {
    name: "ProjectConfigSelectize",
    props: ['customProject', 'project', 'employerId'],
    components: {InputSelectize, SkillsSelectize},
    methods: {
        getDefaultSkills(customProject) {
            return (customProject.skills) ? customProject.skills.map((s) => s.id) : skillSelectize.getDefaultSkills(this.project.skills);
        },
        getProjectSkillLevelsCfg() {
            const skillLevels = this.getSkillLevelNumbersFromBits(this.project.skillLevelBits);
            const cfg = {
                maxItems: 1,
                options: Object
                    .entries(this.globalData.SKILL_LEVEL)
                    .filter(([key, level]) => skillLevels.includes(key))
                    .map(([key, level]) => ({value: key, text: level.title}))
            };
            return cfg;
        },
        openCustomProject(customProject, e) {
            e.preventDefault();
            window.open(customProjectUtil.getLink(customProject), '_blank').focus();
        },
        getSkillLevelRef() {
            return `modalJobCustomProject-skillBits-${this.customProject.id}`;
        },
        getSkillLevelTargetEl() {
            return this.$refs[this.getSkillLevelRef()].targetEl;
        }
    },
}
</script>