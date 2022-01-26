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
                    placeholder="Roles: All" :cfg="projectFunctionsCfg" @selected="setRoles($event)"
                />
            </div>
            <div class="col-md-3">
                <InputSelectize
                    ref="projectSkills"
                    elId="projectSkills"
                    :isParseAsInt="true"
                    placeholder="Skills: All" :cfg="projectSkillsCfg" @selected="setSkills($event)"
                />
            </div>
            <div class="col-md-3">
                <InputSelectize
                    ref="projectSkillLevels"
                    elId="projectSkillLevels"
                    :isParseAsInt="true"
                    placeholder="Experience Levels: All" :cfg="projectSkillLevelsCfg" @selected="setSkillLevels($event)"
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
    data() {
        return {
            filter: {}
        }
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
                options: Object.entries(this.globalData.SKILL_LEVEL).map(([key, level]) => ({value: key, text: level.title}))
            }
        }
    },
    methods: {
        setRoles(roles) {
            this.filter.roles = roles;
            dataUtil.setQueryParams([{key: 'role', val: roles}]);
        },
        setSkills(skills) {
            this.filter.skills = skills;
            dataUtil.setQueryParams([{key: 'skill', val: skills}]);
        },
        setSkillLevels(levels) {
            this.filter.skillLevels = levels;
            dataUtil.setQueryParams([{key: 'level', val: levels}]);
        }
    },
    mounted() {
        dataUtil.setSkillLevels(this.initData.projects, this.globalData);
        const queryParams = dataUtil.getQueryParams();
        this.$refs.projectFunction.elSel.setValue(queryParams.role);
        this.$refs.projectSkills.elSel.setValue(queryParams.skill);
        this.$refs.projectSkillLevels.elSel.setValue(queryParams.level);
    }
}
</script>