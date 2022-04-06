<template>
    <BasePage>
        <div class="card-custom">
            <div class="row mb-3 mt-3">
                <p>
                    Hi {{globalData.uproveUser.firstName}}! Welcome to Uprove!
                </p>
                <p>
                    At Uprove we help individuals like you showcase their talent and connect with employers seeking candidates
                    with your skill set. Complete one or more of our skills based exercises to show employers what you're
                    made of and secure your next opportunity!
                </p>
                <p>
                    To get started select one or more roles you're interested in and we'll recommend projects
                    that you can complete to submit to employers:
                </p>
            </div>
            <div class="row mb-3 ms-3 me-3 justify-content-center">
                <div v-for="role in sortedRoles" class="col-md-2 col-6 p-2">
                    <button
                        @click="toggleSelection($event, role.id)"
                        class="btn btn-secondary w-100 h-100"
                        style="min-height: 60px;"
                    >
                        {{role.name}}
                    </button>
                </div>
                <div class="mt-3">
                    <button
                        class="btn btn-primary w-100"
                        :disabled="(selectedRoleIds.length) ? null : true"
                        :title="(selectedRoleIds.length) ? null : 'Select one or more roles to begin'"
                        @click="openProjectsPage"
                    >
                        View recommended projects <i v-if="selectedRoleIds.length" class="fas fa-arrow-right"></i>
                    </button>
                </div>
            </div>
        </div>
    </BasePage>
</template>

<script>
import BannerAlert from "../../components/BannerAlert";
import dataUtil from "../../../utils/data";
import PageHeader from "../../components/PageHeader";
import BasePage from "../base/BasePage";

export default {
    name: "CandidateOnboardPage",
    components: {BasePage, BannerAlert, PageHeader},
    data() {
        return {
            selectedRoleIds: []
        }
    },
    computed: {
        sortedRoles() {
            return dataUtil.sortBy(this.initData.roles, 'name');
        }
    },
    methods: {
        toggleSelection(e, roleId) {
            const initialLength = this.selectedRoleIds.length;

            // Remove the ID if it's already in the list
            this.selectedRoleIds = this.selectedRoleIds.filter((rId) => rId !== roleId);

            // Add the ID if it's new
            if (initialLength === this.selectedRoleIds.length) {
                this.selectedRoleIds.push(roleId);
            }

            // Toggle the button on/off
            const targetEl$ = $(e.currentTarget);
            targetEl$.toggleClass('btn-secondary');
            targetEl$.toggleClass('btn-info');
        },
        openProjectsPage() {
            dataUtil.setQueryParams([{key: 'role', val: this.selectedRoleIds}], '/projects/');
        }
    }
}
</script>