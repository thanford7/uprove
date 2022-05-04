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
                                <div v-for="p in candidate.userProjects" class="mb-2">
                                    <button type="button" class="btn btn-info text-start w-75" @click="redirectUrl(`/user-project/${p.id}/`, true)">
                                        <div class="row">
                                            <div class="col-10 border-end">
                                                <div>
                                                    {{p.role}}: {{p.projectTitle}}
                                                    <template v-if="p.evaluationScorePct">
                                                        <InfoToolTip
                                                            :elId="getNewElUid()"
                                                            :content="getEvalPopoverHtml()"
                                                            :isHtmlContent="true"
                                                            :isExcludeInfoCircle="true"
                                                        >
                                                            <span
                                                                class="badge rounded-pill"
                                                                :class="`bg-${getBadgeColor({score: p.evaluationScorePct})}`"
                                                            >{{p.evaluationScorePct}}%</span>
                                                        </InfoToolTip>
                                                    </template>
                                                </div>
                                                <div>
                                                    <BadgesSkillLevels :skillLevels="p.skillLevels"/>
                                                </div>
                                                <div>
                                                    <BadgesSkills :skills="p.skills"/>
                                                </div>
                                            </div>
                                            <div class="col-2 d-flex align-items-center">
                                                <div>
                                                    <i
                                                        class="fas fa-external-link-alt fa-2x align-middle -color-white-text -color-hover-moderategrey-text"
                                                        title="View project in new tab"
                                                    >
                                                    </i>
                                                </div>
                                            </div>
                                        </div>
                                    </button>
                                </div>
                            </td>
                            <td>
                                <a
                                    v-if="globalData?.uproveUser?.leverUserKey" href="#"
                                    @click="eventBus.emit('open:addLeverOpportunityModal', candidate)"
                                >
                                    Add to Lever
                                </a>
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
        BannerAlert, InfoToolTip, PageHeader, RolesSelectize, SkillLevelsSelectize, SkillsSelectize, Table
    },
    data() {
        return {
            headers: [[
                {'value': 'Name', 'sortFn': 'firstName'},
                {'value': 'Projects'},
                {'value': 'Actions'}
            ]]
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
                    || this.filter.skillLevelBits
                );
                if (hasFilter && !candidate.userProjects.length) {
                    return filteredCandidates;
                }
                if (!hasFilter) {
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
                    const hasSkillLevel = (
                        !this.filter.skillLevelBits
                        || (this.filter.skillLevelBits & up.skillLevelBit)
                    );
                    return hasRole && hasSkill && hasSkillLevel;
                });
                if (!candidate.userProjects.length) {
                    return filteredCandidates;
                }
                filteredCandidates.push(candidate);
                return filteredCandidates;
            }, []);
        }
    },
    methods: {
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
        setSkills(skillIds) {
            this.filter.skills = this.$refs.skills.getSkills(skillIds);
            dataUtil.setQueryParams([{key: 'skill', val: skillIds}]);
        },
    },
    mounted() {
        this.initData.candidates.forEach((c) => {
            skillLevelSelectize.setSkillLevels(c.userProjects, true);
            c.userProjects.forEach((up) => {
                if (up.evaluationCriteria) {
                    up.evaluationScorePct = userProjectUtil.getEvaluationScore(up.evaluationCriteria);
                }
            });
        });
    }
}
</script>