<template>
    <BannerAlert :alerts="alerts"/>
    <div>
        <div class="row mt-3">
            <h1>Admin Page</h1>
            <h3>Create</h3>
            <div class="col-md-3 me-2 mb-2">
                <button type="button" class="btn btn-secondary" style="width: 100%;" @click="eventBus.emit('open:editEmployerModal')">Employer account</button>
            </div>
            <div class="col-md-3 me-2 mb-2">
                <button type="button" class="btn btn-secondary" style="width: 100%;" @click="eventBus.emit('open:editProjectModal')">Project</button>
            </div>
            <div class="col-md-3 me-2 mb-2">
                <button type="button" class="btn btn-secondary" style="width: 100%;" @click="eventBus.emit('open:editUserModal')">User</button>
            </div>
        </div>
        <div class="row mt-3 mb-3">
            <h3>Edit</h3>
            <div class="col-md-3 me-2">
                <InputSelectize
                    ref="sel1"
                    elId="editEmployer"
                    placeholder="Select employer"
                    :cfg="employerCfg"
                    :isParseAsInt="true"
                    @selected="selectedEmployer = openEditEmployerModal.bind(this)($event)"
                />
            </div>
            <div class="col-md-3 me-2">
                <InputSelectize
                    ref="sel2"
                    elId="editProject"
                    placeholder="Select project"
                    :cfg="projectCfg"
                    :isParseAsInt="true"
                    @selected="selectedProject = openEditProjectModal.bind(this)($event)"
                />
            </div>
            <div class="col-md-3 me-2">
                <InputSelectize
                    ref="sel3"
                    elId="editUser"
                    placeholder="Select user"
                    :cfg="userCfg"
                    :isParseAsInt="true"
                    @selected="selectedUser = openEditUserModal.bind(this)($event)"
                />
            </div>
        </div>
    </div>
    <EditEmployerModal/>
    <EditUserModal/>
</template>

<script>
import BannerAlert from "../../components/BannerAlert";
import EditEmployerModal from "../../modals/EditEmployerModal";
import EditUserModal from "../../modals/EditUserModal";
import InputSelectize from "../../inputs/InputSelectize";

export default {
    name: "AdminPage.vue",
    components: {BannerAlert, EditEmployerModal, EditUserModal, InputSelectize},
    computed: {
        employerCfg() {
            return {
                maxItems: 1,
                options: this.initData.employers.map((e) => ({value: e.id, text: e.companyName}))
            }
        },
        projectCfg() {
            return {
                maxItems: 1,
                options: this.initData.projects.map((p) => ({value: p.id, text: p.title}))
            }
        },
        userCfg() {
            return {
                maxItems: 1,
                options: this.initData.users.map((u) => ({value: u.id, text: `${u.firstName} ${u.lastName} (${u.id})`}))
            }
        }
    },
    methods: {
        getEmployer(employerId) {
            return this.initData.employers.find((e) => e.id === employerId);
        },
        getProject(projectId) {
            return this.initData.projects.find((p) => p.id === projectId);
        },
        getUser(userId) {
            return this.initData.users.find((u) => u.id === userId);
        },
        openEditEmployerModal(employerId) {
            if (!employerId) {
                return;
            }
            this.eventBus.emit('open:editEmployerModal', this.getEmployer(employerId));
            const sel = this.$refs['sel1'];
            sel.elSel.clear(true);
        },
        openEditProjectModal(projectId) {
            if (!projectId) {
                return;
            }
            this.eventBus.emit('open:editProjectModal', this.getProject(projectId));
            const sel = this.$refs['sel2'];
            sel.elSel.clear(true);
        },
        openEditUserModal(userId) {
            if (!userId) {
                return;
            }
            const sel = this.$refs['sel3'];
            sel.elSel.clear(true);
            this.eventBus.emit('open:editUserModal', this.getUser(userId));
        },
    },
    mounted() {
        this.eventBus.on('ajaxSuccess', () => {
            this.alerts.push({
                message: 'Success',
                alertType: 'success'
            });
        });
        this.eventBus.on('ajaxFailure', ({xhr, textStatus, errorThrown}) => {
            this.alerts.push({
                message: `Failure: ${errorThrown}`,
                alertType: 'danger'
            });
        });
    }
}
</script>