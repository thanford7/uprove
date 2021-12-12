<template>
    <BannerAlert :alerts="alerts"/>
    <div class="container-lg">
        <div class="row mt-3">
            <h1>Admin Page</h1>
            <h3>Create</h3>
            <div class="col-md-3 me-2 mb-2">
                <button type="button" class="btn btn-secondary" style="width: 100%;" @click="eventBus.emit('open:editEmployerModal')">Employer account</button>
            </div>
            <div class="col-md-3 me-2 mb-2">
                <button type="button" class="btn btn-secondary" style="width: 100%;" @click="openEditProjectModal.bind(this)(null, false)">Project</button>
            </div>
            <div class="col-md-3 me-2 mb-2">
                <button type="button" class="btn btn-secondary" style="width: 100%;" @click="eventBus.emit('open:editUserModal')">User</button>
            </div>
            <div class="col-md-3 me-2 mb-2">
                <button type="button" class="btn btn-secondary" style="width: 100%;" @click="eventBus.emit('open:editFunctionModal')">Function</button>
            </div>
            <div class="col-md-3 me-2 mb-2">
                <button type="button" class="btn btn-secondary" style="width: 100%;" @click="eventBus.emit('open:editSkillModal')">Skill</button>
            </div>
        </div>
        <div class="row mt-3 mb-3">
            <h3>Edit</h3>
            <div class="col-md-3 me-2">
                <InputSelectize
                    ref="editEmployer"
                    elId="editEmployer"
                    placeholder="Select employer"
                    :cfg="employerCfg"
                    :isParseAsInt="true"
                    @selected="openEditEmployerModal.bind(this)($event)"
                />
            </div>
            <div class="col-md-3 me-2">
                <InputSelectize
                    ref="editProject"
                    elId="editProject"
                    placeholder="Select project"
                    :cfg="projectCfg"
                    :isParseAsInt="true"
                    @selected="openEditProjectModal.bind(this)($event, true)"
                />
            </div>
            <div class="col-md-3 me-2">
                <InputSelectize
                    ref="editUser"
                    elId="editUser"
                    placeholder="Select user"
                    :cfg="userCfg"
                    :isParseAsInt="true"
                    @selected="openEditUserModal.bind(this)($event)"
                />
            </div>
            <div class="col-md-3 me-2">
                <InputSelectize
                    ref="editFunction"
                    elId="editFunction"
                    placeholder="Select function"
                    :cfg="functionCfg"
                    :isParseAsInt="true"
                    @selected="openEditFunctionModal.bind(this)($event)"
                />
            </div>
            <div class="col-md-3 me-2">
                <InputSelectize
                    ref="editSkill"
                    elId="editSkill"
                    placeholder="Select skill"
                    :cfg="skillCfg"
                    :isParseAsInt="true"
                    @selected="openEditSkillModal.bind(this)($event)"
                />
            </div>
        </div>
    </div>
    <EditEmployerModal/>
    <EditFunctionModal/>
    <EditProjectModal/>
    <EditSkillModal/>
    <EditUserModal/>
</template>

<script>
import BannerAlert from "../../components/BannerAlert";
import EditEmployerModal from "../../modals/EditEmployerModal";
import EditFunctionModal from "../../modals/EditFunctionModal";
import EditProjectModal from "../../modals/EditProjectModal";
import EditSkillModal from "../../modals/EditSkillModal";
import EditUserModal from "../../modals/EditUserModal";
import InputSelectize from "../../inputs/InputSelectize";

export default {
    name: "AdminPage.vue",
    components: {BannerAlert, EditEmployerModal, EditFunctionModal, EditProjectModal, EditSkillModal, EditUserModal, InputSelectize},
    watch: {
        initData: {
            deep: true,
            handler(initData) {
                [
                    ['editEmployer', this.getEmployerOptions],
                    ['editFunction', this.getProjectFunctionOptions],
                    ['editProject', this.getProjectOptions],
                    ['editSkill', this.getProjectSkillOptions],
                    ['editUser', this.getUserOptions]
                ].forEach(([ref, optionFn]) => {
                    const sel = this.$refs[ref].elSel;
                    sel.clearOptions(true);
                    sel.addOption(optionFn());
                    sel.refreshOptions(false);
                })
            }
        }
    },
    computed: {
        employerCfg() {
            return {
                maxItems: 1,
                sortField: 'text',
                options: this.getEmployerOptions()
            }
        },
        functionCfg() {
            return {
                maxItems: 1,
                sortField: 'text',
                options: this.getProjectFunctionOptions()
            }
        },
        projectCfg() {
            return {
                maxItems: 1,
                sortField: 'text',
                options: this.getProjectOptions()
            }
        },
        skillCfg() {
            return {
                maxItems: 1,
                sortField: 'text',
                options: this.getProjectSkillOptions()
            }
        },
        userCfg() {
            return {
                maxItems: 1,
                sortField: 'text',
                options: this.getUserOptions()
            }
        }
    },
    methods: {
        getEmployer(employerId) {
            // Copy so the form doesn't mutate the original data
            return Object.assign({}, this.initData.employers.find((e) => e.id === employerId));
        },
        getEmployerOptions() {
            return this.initData.employers.map((e) => ({value: e.id, text: e.companyName}));
        },
        getProject(projectId) {
            return Object.assign({}, this.initData.projects.find((p) => p.id === projectId));
        },
        getProjectOptions() {
            return this.initData.projects.map((p) => ({value: p.id, text: p.title}));
        },
        getProjectFunction(functionId) {
            return Object.assign({}, this.initData.functions.find((f) => f.id === functionId));
        },
        getProjectFunctionOptions() {
            return this.initData.functions.map((f) => ({value: f.id, text: f.functionName}));
        },
        getProjectSkill(skillId) {
            return Object.assign({}, this.initData.skills.find((s) => s.id === skillId));
        },
        getProjectSkillOptions() {
            return this.initData.skills.map((s) => ({value: s.id, text: s.skillName}));
        },
        getUser(userId) {
            return Object.assign({}, this.initData.users.find((u) => u.id === userId));
        },
        getUserOptions() {
            return this.initData.users.map((u) => ({value: u.id, text: `${u.firstName} ${u.lastName} (${u.id})`}));
        },
        openEditEmployerModal(employerId) {
            if (!employerId) {
                return;
            }
            this.eventBus.emit('open:editEmployerModal', this.getEmployer(employerId));
            const sel = this.$refs['editEmployer'];
            sel.elSel.clear(true);
        },
        openEditFunctionModal(functionId) {
            if (!functionId) {
                return;
            }
            this.eventBus.emit('open:editFunctionModal', this.getProjectFunction(functionId));
            const sel = this.$refs['editFunction'];
            sel.elSel.clear(true);
        },
        openEditProjectModal(projectId, isEdit) {
            if (!projectId && isEdit) {
                return;
            }
            this.eventBus.emit('open:editProjectModal', {
                formData: this.getProject(projectId),
                employers: this.initData.employers
            });
            const sel = this.$refs['editProject'];
            sel.elSel.clear(true);
        },
        openEditSkillModal(skillId) {
            if (!skillId) {
                return;
            }
            this.eventBus.emit('open:editSkillModal', this.getProjectSkill(skillId));
            const sel = this.$refs['editSkill'];
            sel.elSel.clear(true);
        },
        openEditUserModal(userId) {
            if (!userId) {
                return;
            }
            const sel = this.$refs['editUser'];
            sel.elSel.clear(true);
            this.eventBus.emit('open:editUserModal', {formData: this.getUser(userId)});
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