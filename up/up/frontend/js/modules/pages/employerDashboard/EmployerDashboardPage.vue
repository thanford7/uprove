<template>
    <div class="container-lg">
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
                            <th colspan="3"></th>
                            <th colspan="4" class="text-center border-start">Applicants</th>
                        </tr>
                        <tr>
                            <th></th>
                            <th>Job title</th>
                            <th>Status</th>
                            <th class="text-center border-start">Invited</th>
                            <th class="text-center">Applied</th>
                            <th class="text-center">Selected</th>
                            <th class="text-center">Declined</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="job in initData.employer.jobs" class="hover-menu">
                            <td>
                                <span
                                    class="hover-show" title="Edit job"
                                    @click="eventBus.emit('open:editJobPostingModal', job)"
                                ><font-awesome-icon :icon="['fas', 'pencil-alt']"/></span>
                                <span
                                    class="hover-show" title="Invite applicants"
                                    @click="eventBus.emit('open:inviteJobApplicantModal', job)"
                                ><font-awesome-icon :icon="['fas', 'user-plus']"/></span>
                            </td>
                            <td>{{job.jobTitle}}</td>
                            <td>{{getJobStatus(job)}}</td>
                            <td class="text-center border-start">{{job.applications.filter((a) => !Boolean(a.submissionDateTime)).length}}</td>
                            <td class="text-center">{{job.applications.filter((a) => Boolean(a.submissionDateTime)).length}}</td>
                            <td class="text-center">{{job.applications.filter((a) => Boolean(a.approveDateTime)).length}}</td>
                            <td class="text-center">{{job.applications.filter((a) => Boolean(a.declineDateTime)).length}}</td>
                        </tr>
                        <tr v-if="!initData.employer.jobs.length">
                            <td colspan="7">Post your first job</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="col-md-9 card-custom">
                <h3>Applicants</h3>
            </div>
        </div>
        <EditJobPostingModal/>
        <InviteJobApplicantModal/>
    </div>
</template>

<script>
import EditJobPostingModal from "../../modals/EditJobPostingModal";
import InviteJobApplicantModal from "../../modals/InviteJobApplicantModal";

export default {
    name: "EmployerDashboardPage.vue",
    components: {EditJobPostingModal, InviteJobApplicantModal},
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