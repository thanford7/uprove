<template>
    <InfoToolTip :elId="getNewElUid()" :isExcludeInfoCircle="true" content="This employer accepts Uprove profiles for a job application. Apply with a single click!">
        <button class="btn btn-primary" :class="btnClasses" @click="saveChange">
            <i class="fas fa-bolt -color-yellow-text"></i>&nbsp; Fast apply
        </button>
    </InfoToolTip>
</template>

<script>
import InfoToolTip from "../../components/InfoToolTip";

export default {
    name: "FastApplyBtn",
    props: ['btnClasses', 'job'],
    components: {InfoToolTip},
    data() {
        return {
            crudUrl: 'user-job-application/',
            pageRedirect: '/candidateDashboard/?tab=applications'
        }
    },
    methods: {
        readForm() {
            return {
                userId: this.globalData.uproveUser.id,
                employerJobId: this.job.id
            }
        }
    }
}
</script>