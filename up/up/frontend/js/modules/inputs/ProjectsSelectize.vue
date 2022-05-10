<template>
    <InputSelectize
        ref="projects"
        :elId="getNewElUid()"
        :isParseAsInt="true"
        placeholder="Required"
        :cfg="projectsCfg"
        @selected="updateCustomProjects"
    />
</template>

<script>
import dataUtil from "../../utils/data";
import InputSelectize from "./InputSelectize";
import skillSelectize from "../selectizeCfgs/skill";

export default {
    name: "ProjectsSelectize",
    components: {InputSelectize},
    props: ['isAllowMulti', 'employerId', 'jobId', 'allowedProjects'],
    data() {
        return {
            newProjectCount: 0,
        }
    },
    computed: {
        projectsCfg() {
            const plugins = ['uprove'];
            if (this.isAllowMulti) {
                plugins.push('remove_button');
            }
            return {
                plugins,
                maxItems: (this.isAllowMulti) ? null : 1,
                optgroupValueField: 'role',
                optgroupLabelField: 'role',
                optgroupField: 'role',
                valueField: 'id',
                labelField: 'title',
                searchField: ['title', 'role'],
                closeAfterSelect: true,
                render: {
                    option: (data, escape) => {
                        let skillsHtml = '';
                        data.skills.forEach((skill) => {
                            skillsHtml += `<div class="badge -color-lightblue -color-black-text me-1">${escape(skill.name)}</div>`
                        });
                        let skillLevelsHtml = '';
                        this.getSkillLevelsFromBits(data.skillLevelBit).forEach((skillLevel) => {
                            skillLevelsHtml += `<div class="badge -color-lightgrey -color-black-text me-1">${escape(skillLevel.title)}</div>`
                        });
                        const getProjectUrl = (projectId) => `/project/${projectId}/`;
                        return `
                            <div class="option" data-selectable data-value="${data.id}" style="cursor: pointer;">
                                <div class="mb-1">
                                    ${escape(data.title)}
                                    <a href="${getProjectUrl(data.id)}" title="Open full project description"><i class="fas fa-external-link-alt"></i></a>
                                </div>
                                <div class="-sub-text">${data.description}</div>
                                <div><span class="-sub-text">Skills: </span>${skillsHtml}</div>
                                <div class="mt-1"><span class="-sub-text">Role level: </span>${skillLevelsHtml}</div>
                            </div>
                        `;
                    }
                }
            };
        }
    },
    methods: {
        getNewCustomProject(projectId) {
            const proj = this.getProject(projectId);
            const customProject = {
                id: `new-${this.newProjectCount}`,
                projectId,
                skillIds: skillSelectize.getDefaultSkills(proj.skills),
            };
            this.newProjectCount++;
            return customProject;
        },
        getProject(projectId) {
            return this.cData.projects.find((project) => project.id === projectId);
        },
        setAllowedProjects() {
            this.$refs.projects.elSel.setValue((this.allowedProjects || []).map((ap) => ap.projectId), true);
        },
        updateCustomProjects(projectIds) {
            if (!this.isAllowMulti) {
                const customProject = this.getNewCustomProject(projectIds);
                this.$emit('projectChange', customProject);
            }
            // Remove projects that are no longer selected
            if (projectIds && !Array.isArray(projectIds)) {
                projectIds = [projectIds]
            }
            projectIds = projectIds || [];
            const removedProjects = (this.allowedProjects|| []).filter((ap) => !projectIds.includes(ap.projectId));
            if (removedProjects.length) {
                removedProjects.forEach((p) => {
                    dataUtil.removeItemFromList((this.allowedProjects|| []), (item) => item.id === p.id);
                });
            }

            // Add new projects
            const currentProjectIds = this.allowedProjects.map((ap) => ap.projectId);
            projectIds.forEach((projectId) => {
                if (!currentProjectIds.includes(projectId)) {
                    this.allowedProjects.push(this.getNewCustomProject(projectId))
                }
            });

            const projects = (this.isAllowMulti) ? this.allowedProjects : (this.allowedProjects?.length) ? this.allowedProjects[0] : null;
            this.$emit('projectChange', projects);
        },
        getTargetEl() {
            return this.$refs.projects.targetEl;
        }
    },
    async mounted() {
        let route = `project/?employerId=${this.employerId}`;
        if (this.jobId) {
            route += `&jobId=${this.jobId}`
        }
        await this.loadData([{route, dataKey: 'projects'}]);
        const optionGroups = dataUtil.sortBy(dataUtil.uniqBy(this.cData.projects.map((p) => ({key: p.role, data: {role: p.role}})), 'key'), 'key');
        this.$refs.projects.resetOptions(this.cData.projects, optionGroups);
        this.setAllowedProjects();
    },
    updated() {
        this.setAllowedProjects();
    }
}
</script>