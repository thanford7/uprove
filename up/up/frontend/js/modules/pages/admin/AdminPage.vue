<template>
    <div class="container-lg">
        <BannerAlert/>
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
                <button type="button" class="btn btn-secondary" style="width: 100%;" @click="eventBus.emit('open:editRoleModal')">Role</button>
            </div>
            <div class="col-md-3 me-2 mb-2">
                <button type="button" class="btn btn-secondary" style="width: 100%;" @click="eventBus.emit('open:editSkillModal')">Skill</button>
            </div>
            <div class="col-md-3 me-2 mb-2">
                <button type="button" class="btn btn-secondary" style="width: 100%;" @click="eventBus.emit('open:editJobTemplateModal')">Job template</button>
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
                    ref="editRole"
                    elId="editRole"
                    placeholder="Select role"
                    :cfg="roleCfg"
                    :isParseAsInt="true"
                    @selected="openEditRoleModal.bind(this)($event)"
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
            <div class="col-md-3 me-2">
                <InputSelectize
                    ref="editJobTemplate"
                    elId="editJobTemplate"
                    placeholder="Select job template"
                    :cfg="templateCfg"
                    :isParseAsInt="true"
                    @selected="openEditJobTemplateModal.bind(this)($event)"
                />
            </div>
        </div>
    </div>
    <EditEmployerModal/>
    <EditRoleModal/>
    <EditJobTemplateModal/>
    <EditProjectModal/>
    <EditSkillModal/>
    <EditUserModal :isShowAdminFields="true"/>
</template>

<script>
import BannerAlert from "../../components/BannerAlert";
import EditEmployerModal from "../../modals/EditEmployerModal";
import EditRoleModal from "../../modals/EditRoleModal";
import EditJobTemplateModal from "../../modals/EditJobTemplateModal";
import EditProjectModal from "../../modals/EditProjectModal";
import EditSkillModal from "../../modals/EditSkillModal";
import EditUserModal from "../../modals/EditUserModal";
import InputSelectize from "../../inputs/InputSelectize";

export default {
    name: "AdminPage.vue",
    components: {
        BannerAlert, EditEmployerModal, EditRoleModal, EditProjectModal, EditJobTemplateModal,
        EditSkillModal, EditUserModal, InputSelectize
    },
    watch: {
        initData: {
            deep: true,
            handler(initData) {
                [
                    ['editEmployer', this.getEmployerOptions],
                    ['editRole', this.getRoleOptions],
                    ['editJobTemplate', this.getJobTemplateOptions],
                    ['editProject', this.getProjectOptions],
                    ['editSkill', this.getSkillOptions],
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
        roleCfg() {
            return {
                maxItems: 1,
                sortField: 'text',
                options: this.getRoleOptions()
            }
        },
        templateCfg() {
            return {
                maxItems: 1,
                sortField: 'text',
                options: this.getJobTemplateOptions()
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
                options: this.getSkillOptions()
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
        getJobTemplate(templateId) {
            return Object.assign({}, this.initData.jobTemplates.find((jt) => jt.id === templateId));
        },
        getJobTemplateOptions() {
            return this.initData.jobTemplates.map((e) => ({value: e.id, text: e.title}));
        },
        getProject(projectId) {
            return Object.assign({}, this.initData.projects.find((p) => p.id === projectId));
        },
        getProjectOptions() {
            return this.initData.projects.map((p) => ({value: p.id, text: p.title}));
        },
        getRole(roleId) {
            return Object.assign({}, this.initData.roles.find((r) => r.id === roleId));
        },
        getRoleOptions() {
            return this.initData.roles.map((r) => ({value: r.id, text: r.name}));
        },
        getSkill(skillId) {
            return Object.assign({}, this.initData.skills.find((s) => s.id === skillId));
        },
        getSkillOptions() {
            return this.initData.skills.map((s) => ({value: s.id, text: s.name}));
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
        openEditRoleModal(roleId) {
            if (!roleId) {
                return;
            }
            this.eventBus.emit('open:editRoleModal', this.getRole(roleId));
            const sel = this.$refs.editRole;
            sel.elSel.clear(true);
        },
        openEditJobTemplateModal(templateId) {
            if (!templateId) {
                return;
            }
            this.eventBus.emit('open:editJobTemplateModal', this.getJobTemplate(templateId));
            const sel = this.$refs['editJobTemplate'];
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
            this.eventBus.emit('open:editSkillModal', this.getSkill(skillId));
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
}
</script>