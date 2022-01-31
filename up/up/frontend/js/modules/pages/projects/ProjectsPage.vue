<template>
    <div class="container-lg">
        <div class="row mt-3 mb-3">
            <h1>Projects</h1>
        </div>
        <div class="row filter mb-3">
            <div class="col-md-3">
                <InputSelectize
                    ref="role"
                    elId="role"
                    :isParseAsInt="true"
                    placeholder="Roles: All" :cfg="rolesCfg" @selected="setRoles($event)"
                />
            </div>
            <div class="col-md-3">
                <InputSelectize
                    ref="skills"
                    elId="skills"
                    :isParseAsInt="true"
                    placeholder="Skills: All" :cfg="skillsCfg" @selected="setSkills($event)"
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
import dataUtil from "../../../utils/data";
import InputSelectize from "../../inputs/InputSelectize";
import ProjectCard from "../../components/ProjectCard";
import skillLevelSelectize from "../../selectizeCfgs/skillLevels";
import skillSelectize from "../../selectizeCfgs/skill";

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
                if (this.filter.roles && this.filter.roles.length && !this.filter.roles.includes(project.roleId)) {
                    return filteredProjects;
                }
                if (this.filter.skills && this.filter.skills.length
                    && !project.skills.filter((skill) => this.filter.skills.includes(skill.name)).length
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
        rolesCfg() {
            return {
                plugins: ['remove_button'],
                maxItems: null,
                options: dataUtil.sortBy(this.initData.roles.map((r) => ({value: r.id, text: r.name})), 'text')
            };
        },
        skillsCfg() {
            return skillSelectize.getSkillCfg(this.initData.skills);
        },
        projectSkillLevelsCfg() {
            return skillLevelSelectize.getSkillLevelCfg(this.globalData.SKILL_LEVEL);
        }
    },
    methods: {
        setRoles(roles) {
            this.filter.roles = roles;
            dataUtil.setQueryParams([{key: 'role', val: roles}]);
        },
        setSkills(skillIds) {
            const skills = this.initData.skills.reduce((skills, s) => {
                if (skillIds.includes(s.id)) {
                    skills.push(s.name);
                }
                return skills;
            }, []);
            this.filter.skills = skills;
            dataUtil.setQueryParams([{key: 'skill', val: skills}]);
        },
        setSkillLevels(levels) {
            this.filter.skillLevels = levels;
            dataUtil.setQueryParams([{key: 'level', val: levels}]);
        }
    },
    mounted() {
        skillLevelSelectize.setSkillLevels(this.initData.projects);
        const queryParams = dataUtil.getQueryParams();
        this.$refs.role.elSel.setValue(queryParams.role);
        this.$refs.skills.elSel.setValue(queryParams.skill);
        this.$refs.projectSkillLevels.elSel.setValue(queryParams.level);
    }
}
</script>