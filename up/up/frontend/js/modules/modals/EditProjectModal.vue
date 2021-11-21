<template>
    <BaseModal
        :modalId="modalName"
        :modalTitle="(formData.id) ? `Edit project: ${formData.title} (${formData.id})`: 'Create new project'"
        :primaryButtonText="(formData.id) ? 'Save changes' : 'Create project'"
        :isAllowDelete="Boolean(formData.id)"
        @saveChange="saveChange($event)"
        @deleteObject="deleteObject($event)"
    >
        <div class="mb-3">
            <label for="projectTitle" class="form-label">Title</label>
            <input type="text" class="form-control" placeholder="Required" id="projectTitle" v-model="formData.title">
        </div>
        <div class="mb-3">
            <label for="projectFunction" class="form-label">Role</label>
            <InputSelectize
                ref="projectFunction"
                elId="projectFunction"
                placeholder="Required" :cfg="projectFunctionsCfg" @selected="formData.function = $event"
            />
        </div>
        <div class="mb-3">
            <label for="projectSkills" class="form-label">Skills</label>
            <InputSelectize
                ref="projectSkills"
                elId="projectSkills"
                placeholder="Required" :cfg="projectSkillsCfg" @selected="formData.skills = $event"
            />
        </div>
        <div class="mb-3">
            <label for="projectSkillLevels" class="form-label">Skill levels</label>
            <InputSelectize
                ref="projectSkillLevels"
                elId="projectSkillLevels"
                :isParseAsInt="true"
                placeholder="Required" :cfg="projectSkillLevelsCfg" @selected="formData.skillLevels = $event"
            />
        </div>
        <div class="mb-3">
            <label for="projectEmployer" class="form-label">Employer</label>
            <InputSelectize
                ref="projectEmployer"
                elId="projectEmployer"
                :isParseAsInt="true"
                placeholder="Optional" :cfg="{maxItems: 1}" @selected="formData.employer = $event"
            />
        </div>
        <div class="mb-3">
            <label for="projectDescription" class="form-label">Description</label>
            <InputWsiwyg elId="projectDescription" placeholder="Add a description..." v-model="formData.description"/>
        </div>
        <div class="mb-3">
            <label for="projectFiles" class="form-label">Description</label>
            <InputMedia elId="projectFiles" :mediaTypes="['file', 'video']" @selected="formData.files = $event"/>
        </div>
    </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal";
import InputMedia from "../inputs/InputMedia";
import InputSelectize from "../inputs/InputSelectize";
import InputWsiwyg from "../inputs/InputWsiwyg";

export default {
    name: "EditProjectModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal, InputMedia, InputSelectize, InputWsiwyg},
    data() {
        return {
            modalName: 'editProjectModal',
            crudUrl: 'project/',
            requiredFields: {
                title: '#projectTitle',
                description: '#projectDescription',
                // Add on mounted
                function: null,
                skills: null,
                skillLevels: null
            },
        }
    },
    computed: {
        projectFunctionsCfg() {
            return {
                maxItems: 1,
                options: _.sortBy(Object.entries(this.globalData.SUPPORTED_FUNCTIONS).map(([key, txt]) => ({value: key, text: txt})), ['text'])
            };
        },
        projectSkillsCfg() {
            return {
                maxItems: null,
                options: _.sortBy(Object.entries(this.globalData.SUPPORTED_SKILLS).map(([key, txt]) => ({value: key, text: txt})), ['text'])
            };
        },
        projectSkillLevelsCfg() {
            return {
                maxItems: null,
                options: Object.entries(this.globalData.SKILL_LEVEL).map(([key, txt]) => ({value: key, text: txt}))
            }
        }
    },
    methods: {
        processRawData(rawData) {
            // Set skill levels from bits
            const skillLevels = Object.keys(this.globalData.SKILL_LEVEL)
                .filter((t) => parseInt(t) & rawData.skillLevelBits);
            this.$refs['projectSkillLevels'].elSel.setValue(skillLevels);

            // Update employer selectize with data
            this.$refs['projectEmployer'].elSel.addOption((rawData.employers || []).map((e) => ({value: e.id, text: e.companyName})))
            this.$refs['projectEmployer'].elSel.refreshOptions(false);

            return Object.assign(rawData.formData, {skillLevels});
        },
        processFormData() {
            const formData = this.readForm();
            return Object.assign({}, formData, {skillLevelBits: _.sum(formData.skillLevels)});
        },
        mounted() {
            this.requiredFields.function = this.$refs['projectFunction'].targetEl;
            this.requiredFields.skills = this.$refs['projectSkills'].targetEl;
            this.requiredFields.skillLevels = this.$refs['projectSkillLevels'].targetEl;
        }
    }
}
</script>