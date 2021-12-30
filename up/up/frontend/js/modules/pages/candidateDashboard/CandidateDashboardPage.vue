<template>
    <div class="container-lg">
        <BannerAlert/>
        <div class="row mt-3 mb-3">
            <div class="align-items-center" style="display: flex">
                <img v-if="initData.user.profileImage" :src="initData.user.profileImage" alt="" class="employer-logo">
                <h2 style="display: inline-block; margin-bottom: 0">Dashboard</h2>
            </div>
        </div>
        <div class="row mb-3 justify-content-center">
            <div class="col-md-9 card-custom">
                <h3 style="display: inline-block">Projects</h3>
                <table class="table mt-3">
                    <thead>
                        <tr>
                            <th colspan="2"></th>
                            <th colspan="4" class="text-center border-start">Employers</th>
                        </tr>
                        <tr>
                            <th></th>
                            <th>Project</th>
                            <th class="text-center border-start">Invited</th>
                            <th class="text-center">Applied</th>
                            <th class="text-center">Selected</th>
                            <th class="text-center">Declined</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="userProject in initData.userProjects" class="hover-menu">
                            <td>
                                <span
                                    class="hover-show" title="Edit project"
                                    @click="eventBus.emit('open:editUserProjectModal', userProject)"
                                ><i class="fas fa-pencil-alt"></i></span>
                            </td>
                            <td>{{userProject.customProject.projectTitle}}</td>
                            <td class="text-center border-start">0</td>
                            <td class="text-center">0</td>
                            <td class="text-center">0</td>
                            <td class="text-center">0</td>
                        </tr>
                        <tr v-if="!initData.userProjects.length">
                            <td colspan="6">Start your first project</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="col-md-9 card-custom">
                <h3>Applications</h3>
            </div>
        </div>
    </div>
</template>

<script>
import BannerAlert from "../../components/BannerAlert";
export default {
    name: "CandidateDashboardPage",
    components: {BannerAlert}
}
</script>