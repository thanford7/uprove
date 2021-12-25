<template>
    <div class="container-lg">
        <div class="row mt-3 mb-3">
            <h1>Projects</h1>
        </div>
        <div class="row filter mb-3">
            <div class="col-md-3">
                <InputSelectize
                    ref="projectFunction"
                    elId="projectFunction"
                    :isParseAsInt="true"
                    placeholder="Roles: All" :cfg="projectFunctionsCfg" @selected="filter.roles = $event"
                />
            </div>
            <div class="col-md-3">
                <InputSelectize
                    ref="projectSkills"
                    elId="projectSkills"
                    :isParseAsInt="true"
                    placeholder="Skills: All" :cfg="projectSkillsCfg" @selected="filter.skills = $event"
                />
            </div>
            <div class="col-md-3">
                <InputSelectize
                    ref="projectSkillLevels"
                    elId="projectSkillLevels"
                    :isParseAsInt="true"
                    placeholder="Experience Levels: All" :cfg="projectSkillLevelsCfg" @selected="filter.skillLevels = $event"
                />
            </div>
        </div>
        <div class="row justify-content-center">
            <template v-for="project in filteredProjects">
                <ProjectCard :cardItem="project"></ProjectCard>
            </template>
            <p v-if="!filteredProjects.length" class="float-end" style="width: auto">No projects to display</p>
        </div>
    </div>
</template>

<script>
import InputSelectize from "../../inputs/InputSelectize";
import ProjectCard from "../../components/ProjectCard";
import dataUtil from "../../../utils/data";

export default {
    name: "ProjectsPage.vue",
    components: {InputSelectize, ProjectCard},
    data: {
        filter: {}
    },
    computed: {
        filteredProjects() {
            return this.initData.projects.reduce((filteredProjects, project) => {
                if (this.filter.roles && this.filter.roles.length && !this.filter.roles.includes(project.functionId)) {
                    return filteredProjects;
                }
                if (this.filter.skills && this.filter.skills.length
                    && !project.skills.filter((skill) => this.filter.skills.includes(skill.id)).length
                ) {
                    return filteredProjects;
                }
                if (this.filter.skillLevels && this.filter.skillLevels.length
                    && !this.filter.skillLevels.filter((skillLevel) => skillLevel & project.skillLevelBits).length
                ) {
                    return filteredProjects;
                }
                filteredProjects.push(project);
                return filteredProjects;
            }, [])
        },
        projectFunctionsCfg() {
            return {
                plugins: ['remove_button'],
                maxItems: null,
                options: dataUtil.sortBy(this.initData.functions.map((f) => ({value: f.id, text: f.functionName})), 'text')
            };
        },
        projectSkillsCfg() {
            return {
                plugins: ['remove_button'],
                maxItems: null,
                options: dataUtil.sortBy(this.initData.skills.map((s) => ({value: s.id, text: s.skillName})), 'text')
            };
        },
        projectSkillLevelsCfg() {
            return {
                plugins: ['remove_button'],
                maxItems: null,
                options: Object.entries(this.globalData.SKILL_LEVEL).map(([key, txt]) => ({value: key, text: txt}))
            }
        }
    },
    mounted() {
        this.initData.projects.forEach((project) => {
            project.skillLevels = Object.entries(this.globalData.SKILL_LEVEL).reduce((skillLevels, [skillLevelBit, skillLevel]) => {
                if (skillLevelBit & project.skillLevelBits) {
                    skillLevels.push(skillLevel);
                }
                return skillLevels;
            }, []);
        });
    }
}
</script>