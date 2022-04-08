<template>
    <div v-if="jobs.jobCount">
        <i class="fas fa-lightbulb -color-orange-text"></i>&nbsp;
        <a v-if="isLoggedIn" :href="getUrlWithParams([{key: 'roles', val: jobs.roleTitleIds}], '/jobs/')">{{getJobsText()}}</a>
        <InfoToolTip
            v-else
            :isExcludeInfoCircle="true"
            :elId="getNewElUid()"
            content="Candidates, sign in or create an account to see job openings"
        >
            {{getJobsText()}}
        </InfoToolTip>
    </div>
</template>

<script>
import dataUtil from "../../../utils/data";
import InfoToolTip from "../../components/InfoToolTip";

export default {
    name: "ProjectJobs",
    props: ['jobs'],
    components: {InfoToolTip},
    methods: {
        getUrlWithParams: dataUtil.getUrlWithParams.bind(dataUtil),
        getJobsText() {
            return `${this.pluralize('job opening', this.jobs.jobCount)} ${(this.jobs.jobCount > 1) ? 'are' : 'is'} related to this project`;
        }
    }
}
</script>