<template>
    <BasePage>
        <div class="card-custom">
            <div class="row mb-3 ms-md-2">
                <h5>Create</h5>
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
                    <button type="button" class="btn btn-secondary" style="width: 100%;" @click="eventBus.emit('open:editCourseModal')">Course</button>
                </div>
            </div>
            <div class="row ms-md-2">
                <h5>Edit</h5>
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
                    <SkillsSelectize
                        ref="editSkill"
                        :skills="initData.skills"
                        :cfg="{isMulti: false, isShowRequired: true, placeholder:'Select skill'}"
                        @selected="openEditSkillModal.bind(this)($event)"
                    />
                </div>
                <div class="col-md-3 me-2">
                    <InputSelectize
                        ref="editCourse"
                        elId="editCourse"
                        :cfg="courseCfg"
                        :isParseAsInt="true"
                        @selected="openEditCourseModal.bind(this)($event)"
                    />
                </div>
            </div>
        </div>
    </BasePage>
    <EditCourseModal/>
    <EditEmployerModal :isUpdateDataOverride="false"/>
    <EditRoleModal/>
    <EditProjectModal/>
    <EditSkillModal/>
    <EditUserModal :isShowAdminFields="true" :isUpdateDataOverride="false" :isHardRefreshOverride="true"/>
</template>

<script>
import BannerAlert from "../../components/BannerAlert";
import BasePage from "../base/BasePage";
import EditCourseModal from "../../modals/EditCourseModal";
import EditEmployerModal from "../../modals/EditEmployerModal";
import EditRoleModal from "../../modals/EditRoleModal";
import EditProjectModal from "../../modals/EditProjectModal";
import EditSkillModal from "../../modals/EditSkillModal";
import EditUserModal from "../../modals/EditUserModal";
import employersSelectize from "../../selectizeCfgs/employers";
import InputSelectize from "../../inputs/InputSelectize";
import SkillsSelectize from "../../inputs/SkillsSelectize";
import usersSelectize from "../../selectizeCfgs/users";
import coursesSelectize from "../../selectizeCfgs/courses";

export default {
    name: "AdminPage.vue",
    components: {
        BasePage, SkillsSelectize, BannerAlert, EditCourseModal, EditEmployerModal, EditRoleModal, EditProjectModal,
        EditSkillModal, EditUserModal, InputSelectize
    },
    computed: {
        courseCfg() {
            return coursesSelectize.getCoursesCfg();
        },
        employerCfg() {
            return employersSelectize.getEmployersCfg();
        },
        roleCfg() {
            return {
                maxItems: 1,
                sortField: 'text',
                options: this.getRoleOptions()
            }
        },
        projectCfg() {
            return {
                maxItems: 1,
                sortField: 'text',
                options: this.getProjectOptions()
            }
        },
        userCfg() {
            return usersSelectize.getUsersCfg();
        }
    },
    methods: {
        getCourse(courseId) {
            // Copy so the form doesn't mutate the original data
            return Object.assign({}, this.$refs.editCourse.elSel.options[courseId]);
        },
        getEmployer(employerId) {
            // Copy so the form doesn't mutate the original data
            return Object.assign({}, this.$refs.editEmployer.elSel.options[employerId]);
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
        getUser(userId) {
            return Object.assign({}, this.$refs.editUser.elSel.options[userId]);
        },
        openEditCourseModal(courseId) {
            if (!courseId) {
                return;
            }
            this.eventBus.emit('open:editCourseModal', this.getCourse(courseId));
            this.$refs.editCourse.elSel.clear(true);
        },
        openEditEmployerModal(employerId) {
            if (!employerId) {
                return;
            }
            this.eventBus.emit('open:editEmployerModal', this.getEmployer(employerId));
            this.$refs.editEmployer.elSel.clear(true);
        },
        openEditRoleModal(roleId) {
            if (!roleId) {
                return;
            }
            this.eventBus.emit('open:editRoleModal', this.getRole(roleId));
            this.$refs.editRole.elSel.clear(true);
        },
        openEditProjectModal(projectId, isEdit) {
            if (!projectId && isEdit) {
                return;
            }
            this.eventBus.emit('open:editProjectModal', {
                formData: this.getProject(projectId),
                employers: this.initData.employers
            });
            this.$refs.editProject.elSel.clear(true);
        },
        openEditSkillModal(skillId) {
            if (!skillId) {
                return;
            }
            this.eventBus.emit('open:editSkillModal', this.getSkill(skillId));
            this.$refs.editSkill.elSel.clear(true);
        },
        openEditUserModal(userId) {
            if (!userId) {
                return;
            }
            this.$refs.editUser.elSel.clear(true);
            this.eventBus.emit('open:editUserModal', this.getUser(userId));
        },
    },
}
</script>