<template>
    <BasePage>
        <template v-slot:filter>
            <BaseFilter>
                <div class="col-12">
                    <h6>Search candidates</h6>
                </div>
                <div class="row">
                    <div class="col-12 col-md filter-item">
                        <RolesSelectize
                            ref="role"
                            placeholder="Roles: All"
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
                        <RangeSlider
                            ref="projectScoreFilter"
                            :elId="getNewElUid()"
                            :startingVal="defaultProjectScore"
                            title="Project score"
                            @changed="setFilter($event, 'projectScore')"
                        />
                    </div>
                </div>
            </BaseFilter>
        </template>
        <div class="row mb-3">
            <div class="card-custom card-custom--no-side-margin">
                <Table :data="initData.candidates" :headers="headers" emptyDataMessage="No current profiles">
                    <template v-slot:body>
                        <tr v-for="candidate in filteredCandidates">
                            <td>
                                <a :href="`/profile/${candidate.profileId}/`" title="Candidate profile">
                                    {{candidate.firstName}} {{candidate.lastName}}
                                </a>
                            </td>
                            <td>
                                <template v-if="candidate.primaryProject">
                                    <InfoToolTip
                                        v-if="candidate?.primaryProject?.evaluationScorePct"
                                        :elId="getNewElUid()"
                                        :content="getEvalPopoverHtml()"
                                        :isHtmlContent="true"
                                        :isExcludeInfoCircle="true"
                                    >
                                        <h5>
                                            <span
                                                class="badge rounded-pill"
                                                :class="`bg-${getBadgeColor({score: candidate.primaryProject.evaluationScorePct})}`"
                                            >{{candidate.primaryProject.evaluationScorePct}}%</span>
                                        </h5>
                                    </InfoToolTip>
                                    <InfoToolTip
                                        v-else
                                        :elId="getNewElUid()"
                                        content="A Uprove expert has not evaluated this project yet"
                                        :isExcludeInfoCircle="true"
                                    >
                                        <h5>
                                            <span
                                                class="badge rounded-pill bg-secondary -color-black-text"
                                            >No evaluation</span>
                                        </h5>
                                    </InfoToolTip>
                                </template>
                                <h5 v-else>
                                    <span
                                        class="badge rounded-pill bg-secondary -color-black-text"
                                    >N/A</span>
                                </h5>
                            </td>
                            <td>
                                <div v-if="candidate.primaryProject" class="mb-2">
                                    <button
                                        type="button" class="btn btn-info text-start w-75"
                                        @click="redirectUrl(`/user-project/${candidate.primaryProject.id}/`, true)"
                                    >
                                        <div style="position: relative;">
                                            <div class="pe-3">
                                                {{candidate.primaryProject.role}}: {{candidate.primaryProject.projectTitle}}
                                            </div>
                                            <div>
                                                <BadgesSkillLevels :skillLevels="candidate.primaryProject.skillLevels"/>
                                            </div>
                                            <div>
                                                <BadgesSkills :skills="candidate.primaryProject.skills"/>
                                            </div>
                                            <i
                                                class="fas fa-external-link-alt align-middle -color-white-text -color-hover-moderategrey-text"
                                                title="View project in new tab"
                                                style="position: absolute; top: 0; right: 0;"
                                            >
                                            </i>
                                        </div>
                                        <div class="-text-small">Last updated: {{formatDate(candidate.primaryProject.updateDateTime)}}</div>
                                    </button>
                                </div>
                            </td>
                            <td>
                                <div
                                    v-if="globalData?.uproveUser?.leverUserKey"
                                    class="btn btn-outline-secondary -color-black-text"
                                    @click="eventBus.emit('open:addLeverOpportunityModal', candidate)"
                                >
                                    <img style="max-height: 20px;" :src="globalData.STATIC_URL + 'img/leverLogo.png'">
                                    Add to Lever
                                </div>
                                <div v-if="candidate.appliedJobs.length" class="-text-medium">
                                    <InfoToolTip
                                        :elId="getNewElUid()"
                                        :content="getAppliedJobsHtml(candidate.appliedJobs)"
                                        :isHtmlContent="true"
                                        :isExcludeInfoCircle="true"
                                    >
                                        <i class="fas fa-check-circle -color-green-text"></i>
                                        Has {{pluralize('application', candidate.appliedJobs.length)}}
                                    </InfoToolTip>
                                </div>
                            </td>
                        </tr>
                    </template>
                </Table>
            </div>
        </div>
    </BasePage>
    <AddLeverOpportunityModal v-if="globalData.uproveUser.employerId" :employerId="globalData.uproveUser.employerId"/>
</template>

<script>
import AddLeverOpportunityModal from "../../modals/AddLeverOpportunityModal";
import BadgesSkillLevels from "../../components/BadgesSkillLevels";
import BadgesSkills from "../../components/BadgesSkills";
import BannerAlert from "../../components/BannerAlert";
import BaseFilter from "../base/BaseFilter";
import BasePage from "../base/BasePage";
import dataUtil from "../../../utils/data";
import InfoToolTip from "../../components/InfoToolTip";
import PageHeader from "../../components/PageHeader";
import RangeSlider from "../../components/RangeSlider";
import RolesSelectize from "../../inputs/RolesSelectize";
import SkillLevelsSelectize from "../../inputs/SkillLevelsSelectize";
import SkillsSelectize from "../../inputs/SkillsSelectize";
import skillLevelSelectize from "../../selectizeCfgs/skillLevels";
import Table from "../../components/Table";
import userProjectUtil from "../../../utils/userProject";

export default {
    name: "CandidateBoardPage",
    components: {
        AddLeverOpportunityModal, BaseFilter, BasePage, BadgesSkillLevels, BadgesSkills,
        BannerAlert, InfoToolTip, PageHeader, RangeSlider, RolesSelectize, SkillLevelsSelectize, SkillsSelectize, Table
    },
    data() {
        return {
            headers: [[
                {'value': 'Name', 'sortFn': 'firstName'},
                {'value': 'Score'},
                {'value': 'Project'},
                {'value': 'Actions'}
            ]],
            defaultProjectScore: 60
        }
    },
    computed: {
        filteredCandidates() {
            // TODO: Make this server side to handle larger data sets
            return this.initData.candidates.reduce((filteredCandidates, candidate) => {
                candidate = dataUtil.deepCopy(candidate) // copy so we don't mutate the original
                const hasFilter = (
                    (this.filter.roles && this.filter.roles.length)
                    || (this.filter.skills && this.filter.skills.length)
                    || this.filter.projectScore
                );
                if (hasFilter && !candidate.userProjects.length) {
                    return filteredCandidates;
                }
                if (!hasFilter) {
                    candidate.primaryProject = this.getBestUserProject(candidate.userProjects);
                    filteredCandidates.push(candidate);
                    return filteredCandidates;
                }
                candidate.userProjects = candidate.userProjects.filter((up) => {
                    const hasRole = (
                        !this.filter?.roles?.length
                        || this.filter.roles.includes(up.roleId)
                    );
                    const hasSkill = (
                        !this.filter?.skills?.length
                        || up.skills.filter((skill) => this.filter.skills.includes(skill.name)).length
                    );
                    const isAboveProjectScore = (
                        !this.filter.projectScore
                        || up.evaluationScorePct >= this.filter.projectScore
                    )
                    return hasRole && hasSkill && isAboveProjectScore;
                });
                if (!candidate.userProjects.length) {
                    return filteredCandidates;
                }
                candidate.primaryProject = this.getBestUserProject(candidate.userProjects);
                filteredCandidates.push(candidate);
                return filteredCandidates;
            }, []);
        }
    },
    methods: {
        formatDate: dataUtil.formatDate.bind(dataUtil),
        getBadgeColor: userProjectUtil.getBadgeColor,
        getEvalPopoverHtml: userProjectUtil.getEvalPopoverHtml,
        getAppliedJobsHtml(appliedJobs) {
            let html = '<div>Current jobs</div><ul>';
            appliedJobs.forEach((j) => {
                html += `
                    <li>
                        ${j}
                    </li>
                `
            });
            html += '</ul>';
            return html;
        },
        getBestUserProject(userProjects) {
            if (!userProjects?.length) {
                return null;
            }
            let bestScore = 0;
            return userProjects.reduce((primary, up) => {
                if (!primary) {
                    bestScore = up.evaluationScorePct;
                    return up;
                }
                if (up.evaluationScorePct > bestScore) {
                    return up;
                }
                return primary;
            });
        },
        setSkills(skillIds) {
            this.filter.skills = this.$refs.skills.getSkills(skillIds);
            dataUtil.setQueryParams([{key: 'skill', val: skillIds}]);
        },
    },
    mounted() {
        this.initData.candidates.forEach((c) => {
            skillLevelSelectize.setSkillLevels(c.userProjects, true);
        });
        const {projectScore, role, skill} = dataUtil.getQueryParams();
        this.defaultProjectScore = projectScore || this.defaultProjectScore;
        this.filter.projectScore = this.defaultProjectScore;
        this.$refs.projectScoreFilter.setValue(this.defaultProjectScore);
        this.$refs.role.setInitialRoleIds(role);
        this.$refs.skills.setValue(skill);
    }
}
</script>