<template>
    <BasePage>
        <template v-slot:filter>
            <BaseFilter>
                <div class="col-12">
                    <h6>Search projects</h6>
                </div>
                <div class="row">
                    <div class="col-12 col-md filter-item">
                        <RolesSelectize
                            ref="role"
                            placeholder="Roles: All"
                            :roles="initData.roles"
                            @selected="setFilter($event, 'roles', 'role')"
                        />
                    </div>
                    <div class="col-12 col-md filter-item">
                        <SkillsSelectize
                            ref="skills"
                            :skills="initData.skills"
                            @selected="setSkills($event)"
                        />
                    </div>
                    <div class="col-12 col-md filter-item">
                        <SkillLevelsSelectize
                            ref="projectSkillLevels"
                            placeholder="Experience Levels: All"
                            @selected="setFilter($event, 'skillLevelBits', 'level')"
                        />
                    </div>
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
import ProjectCard from "./ProjectCard";
import RolesSelectize from "../../inputs/RolesSelectize";
import skillLevelSelectize from "../../selectizeCfgs/skillLevels";
import SkillLevelsSelectize from "../../inputs/SkillLevelsSelectize";
import SkillsSelectize from "../../inputs/SkillsSelectize";
import PageHeader from "../../components/PageHeader";
import BaseFilter from "../base/BaseFilter";

export default {
    name: "ProjectsPage.vue",
    components: {
        BaseFilter, BasePage, PageHeader, ProjectCard, RolesSelectize,
        SkillLevelsSelectize, SkillsSelectize
    },
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
                if (this.filter.skillLevelBits && !(this.filter.skillLevelBits & project.skillLevelBit)
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
        skillLevelSelectize.setSkillLevels(this.initData.projects, true);
        const queryParams = dataUtil.getQueryParams();
        this.$refs.role.elSel.setValue(queryParams.role);
        if (!queryParams.role && this.initData.preferredRoles) {
            const roleIds = dataUtil.uniqArray(this.initData.preferredRoles.map((r) => r.roleId));
            this.$refs.role.elSel.setValue(roleIds);
            this.setFilter(roleIds, 'roles', 'role');
        }
        this.$refs.skills.elSel.setValue(queryParams.skill);
        this.$refs.projectSkillLevels.elSel.setValue(queryParams.level);
    }
}
</script>