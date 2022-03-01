<template>
    <div class="container-lg">
        <BannerAlert/>
        <PageHeader title="Candidate Board"/>
        <div class="row mb-3">
            <div class="card-custom">
                <Table :data="initData.candidates" :headers="headers" emptyDataMessage="No current profiles">
                    <template v-slot:body>
                        <tr v-for="candidate in initData.candidates">
                            <td>
                                <a :href="`/profile/${candidate.profileId}/`" title="Candidate profile">{{candidate.firstName}}</a>
                            </td>
                            <td>{{candidate.lastName}}</td>
                            <td>
                                <div v-for="p in candidate.userProjects" class="mb-2">
                                    <button type="button" class="btn btn-info text-start w-75" @click="redirectUrl(`/candidate-project/${p.id}/`, true)">
                                        <div class="row">
                                            <div class="col-10 border-end">
                                                <div>
                                                    {{p.role}}: {{p.projectTitle}}
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
                        </tr>
                    </template>
                </Table>
            </div>
        </div>
    </div>
</template>

<script>
import BadgesSkillLevels from "../../components/BadgesSkillLevels";
import BadgesSkills from "../../components/BadgesSkills";
import BannerAlert from "../../components/BannerAlert";
import PageHeader from "../../components/PageHeader";
import skillLevelSelectize from "../../selectizeCfgs/skillLevels";
import Table from "../../components/Table";

export default {
    name: "CandidateBoardPage",
    components: {BadgesSkillLevels, BadgesSkills, BannerAlert, PageHeader, Table},
    data() {
        return {
            headers: [[
                {'value': 'First name', 'sortFn': 'firstName'},
                {'value': 'Last name', 'sortFn': 'lastName'},
                {'value': 'Projects'},
            ]]
        }
    },
    mounted() {
        this.initData.candidates.forEach((c) => {
            skillLevelSelectize.setSkillLevels(c.userProjects, true)
        });
    }
}
</script>