<template>
    <BasePage headerTitle="Projects">
        <template v-slot:filter>
            <BaseFilter>
                <div class="col-md-3">
                    <RolesSelectize
                        ref="role"
                        placeholder="Roles: All"
                        :roles="initData.roles"
                        @selected="setFilter($event, 'roles', 'role')"
                    />
                </div>
                <div class="col-md-3">
                    <SkillsSelectize
                        ref="skills"
                        :skills="initData.skills"
                        @selected="setSkills($event)"
                    />
                </div>
                <div class="col-md-3">
                    <SkillLevelsSelectize
                        ref="projectSkillLevels"
                        placeholder="Experience Levels: All"
                        @selected="setFilter($event, 'skillLevelBits', 'level')"
                    />
                </div>
            </BaseFilter>
        </template>
        <div class="row justify-content-center">
            <template v-for="project in filteredProjects">
                <ProjectCard :cardItem="project"></ProjectCard>
            </template>
            <p v-if="!filteredProjects.length" class="float-end" style="width: auto">No projects to display</p>
        </div>
    </BasePage>
</template>

<script>
import dataUtil from "../../../utils/data";
import BasePage from "../base/BasePage";
import ProjectCard from "../../components/ProjectCard";
import RolesSelectize from "../../inputs/RolesSelectize";
import skillLevelSelectize from "../../selectizeCfgs/skillLevels";
import SkillLevelsSelectize from "../../inputs/SkillLevelsSelectize";
import SkillsSelectize from "../../inputs/SkillsSelectize";
import PageHeader from "../../components/PageHeader";
import BaseFilter from "../base/BaseFilter";

export default {
    name: "ProjectsPage.vue",
    components: {BaseFilter, BasePage, PageHeader, ProjectCard, RolesSelectize, SkillLevelsSelectize, SkillsSelectize},
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
                if (this.filter.skillLevelBits && !(this.filter.skillLevelBits & project.skillLevelBits)
                ) {
                    return filteredProjects;
                }
                filteredProjects.push(project);
                return filteredProjects;
            }, [])
        },
    },
    methods: {
        setSkills(skillIds) {
            this.filter.skills = this.$refs.skills.getSkills(skillIds);
            dataUtil.setQueryParams([{key: 'skill', val: skillIds}]);
        },
    },
    mounted() {
        skillLevelSelectize.setSkillLevels(this.initData.projects);
        const queryParams = dataUtil.getQueryParams();
        this.$refs.role.elSel.setValue(queryParams.role);
        this.$refs.skills.setValue(queryParams.skill);
        this.$refs.projectSkillLevels.elSel.setValue(queryParams.level);
    }
}
</script>