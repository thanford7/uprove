<template>
    <div>
        <div class="row mt-3 mb-3">
            <div class="align-items-center" style="display: flex">
                <img v-if="initData.employer.logo" :src="initData.employer.logo" alt="" class="employer-logo">
                <h2 style="display: inline-block; margin-bottom: 0">{{initData.employer.companyName}} Dashboard</h2>
            </div>
        </div>
        <div class="row mb-3 justify-content-center">
            <div class="col-md-9 card-custom">
                <h3 style="display: inline-block">Job postings</h3>
                <button type="button" class="btn btn-primary float-end" @click="eventBus.emit('open:editJobPostingModal')">
                    Create job posting
                </button>
                <table class="table mt-3">
                    <thead>
                        <tr>
                            <th colspan="2"></th>
                            <th colspan="3" class="text-center">Applicants</th>
                        </tr>
                        <tr>
                            <th>Job title</th>
                            <th>Status</th>
                            <th>Applied</th>
                            <th>Selected</th>
                            <th>Declined</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="job in initData.employer.jobs">
                            <td>{{job.jobTitle}}</td>
                            <td>{{getJobStatus(job)}}</td>
                            <td>{{job.applications.filter((a) => Boolean(a.submissionDateTime)).length}}</td>
                            <td>{{job.applications.filter((a) => Boolean(a.approveDateTime)).length}}</td>
                            <td>{{job.applications.filter((a) => Boolean(a.declineDateTime)).length}}</td>
                        </tr>
                        <tr v-if="!initData.employer.jobs.length">
                            <td colspan="5">Post your first job</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="col-md-9 card-custom">
                <h3>Applicants</h3>
            </div>
        </div>
        <EditJobPostingModal/>
    </div>
</template>

<script>
import EditJobPostingModal from "../../modals/EditJobPostingModal";

export default {
    name: "EmployerDashboardPage.vue",
    components: {EditJobPostingModal},
    methods: {
        getJobStatus(job) {
            if (job.closeDate) {
                return 'CLOSED';
            }
            if (job.pauseDate) {
                return 'PAUSED';
            }
            if (job.openDate) {
                return 'OPEN'
            }
            return 'DRAFT';
        }
    }
}
</script>