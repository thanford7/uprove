<template>
    <BaseModal
        :modalId="modalName"
        :modalTitle="(formData.id) ? `Edit project: ${formData.title} (${formData.id})`: 'Create new project'"
        :primaryButtonText="(formData.id) ? 'Save changes' : 'Create project'"
        :isAllowDelete="Boolean(formData.id)"
        :isLargeDisplay="true"
        @saveChange="saveChange($event)"
        @deleteObject="deleteObject($event)"
    >
        <div class="mb-3">
            <label for="projectTitle" class="form-label">Title</label>
            <input type="text" class="form-control" placeholder="Required" id="projectTitle" v-model="formData.title">
        </div>
        <div class="mb-3">
            <label for="projectImage" class="form-label">Display Image</label>
            <div v-if="!isImageUpload" class="mb-1">
                <img :src="formData.image" style="height: 40px;"><br>
            </div>
            <InputMedia
                v-if="isImageUpload"
                elId="projectImage"
                :mediaTypes="['image']"
                @selected="formData.image = $event"
            />
            <a v-if="allowImageToggle" href="#" @click="toggleImageUpload">{{(isImageUpload) ? 'Use existing image' : 'Change image' }}</a>
        </div>
        <div class="mb-3">
            <label for="projectFunction" class="form-label">Role</label>
            <InputSelectize
                ref="projectFunction"
                elId="projectFunction"
                :isParseAsInt="true"
                placeholder="Required" :cfg="projectFunctionsCfg" @selected="formData.functionId = $event"
            />
        </div>
        <div class="mb-3">
            <label for="projectSkills" class="form-label">Skills</label>
            <InputSelectize
                ref="projectSkills"
                elId="projectSkills"
                :isParseAsInt="true"
                placeholder="Required" :cfg="projectSkillsCfg" @selected="formData.skillIds = $event"
            />
        </div>
        <div class="mb-3">
            <label for="projectSkillLevels" class="form-label">Skill levels</label>
            <InputSelectize
                ref="projectSkillLevels"
                elId="projectSkillLevels"
                :isParseAsBits="true"
                placeholder="Required" :cfg="projectSkillLevelsCfg" @selected="formData.skillLevelBits = $event"
            />
        </div>
        <div class="mb-3">
            <label for="projectEmployer" class="form-label">Employer</label>
            <InputSelectize
                ref="projectEmployer"
                elId="projectEmployer"
                :isParseAsInt="true"
                placeholder="Optional" :cfg="{maxItems: 1}" @selected="formData.employerId = $event"
            />
        </div>
        <div class="mb-3">
            <label for="projectDescription" class="form-label">Description</label>
            <InputWsiwyg
                elId="projectDescription"
                placeholder="Add a description..."
                v-model="formData.description"
            />
        </div>
        <div class="mb-3">
            <label for="projectDescription" class="form-label">Instructions</label>
            <InputWsiwyg
                elId="projectInstructions"
                placeholder="Add instructions..."
                v-model="formData.instructions"
            />
        </div>
        <div class="mb-3 pt-1 border-top" v-for="(file, fileId, idx) in formData.newFiles">
            <label :for="`projectFile-file-${fileId}`" class="form-label">File {{ idx + 1 }}</label>
            <div v-if="!file.isShowUpload">
                <FileDisplay :file="file" :isUseFileName="true"/>
            </div>
            <InputMedia
                v-if="file.isShowUpload"
                :elId="`projectFile-file-${fileId}`"
                :mediaTypes="['file', 'video']"
                @selected="file.file = $event"
            />
            <input type="text" class="form-control mb-1" placeholder="Title (required)" :id="`projectFile-title-${fileId}`" v-model="file.title">
            <textarea
                rows="3" class="form-control mb-1"
                placeholder="File description"
                :id="`projectFile-description-${fileId}`"
                v-model="file.description"
            />
            <InputSelectize
                :ref="`projectFile-skillBits-${fileId}`"
                :elId="`projectFile-skillBits-${fileId}`"
                :isParseAsBits="true"
                :items="getSkillLevelsFromBits(file.skillLevelBits)"
                placeholder="Required" :cfg="projectSkillLevelsCfg" @selected="file.skillLevelBits = $event"
            />
            <a href="#" @click="removeFileInput(fileId)"><font-awesome-icon :icon="['fas', 'trash']" class="-color-red-fa"/> Remove file</a>
            &nbsp;&nbsp;
            <a v-if="file.oldFile || file.id" href="#" @click="changeFile(fileId)">
                <font-awesome-icon :icon="['fas', 'exchange-alt']"/>
                &nbsp;{{(file.isShowUpload) ? 'Use existing file' : 'Change file'}}
            </a>
        </div>
        <div class="border-top pt-1">
            <a href="#" @click="addFileInput"><font-awesome-icon :icon="['fas', 'plus']" class="-color-green-fa"/> Add new file</a>
        </div>
    </BaseModal>
</template>

<script>
import {severity} from "../../vueMixins";
import BaseModal from "./BaseModal";
import FileDisplay from "../components/FileDisplay";
import InputMedia from "../inputs/InputMedia";
import InputSelectize from "../inputs/InputSelectize";
import InputWsiwyg from "../inputs/InputWsiwyg";
import form from "../../utils/form";
import $ from "jquery";
import _ from 'lodash';

export default {
    name: "EditProjectModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal, FileDisplay, InputMedia, InputSelectize, InputWsiwyg},
    data() {
        return {
            modalName: 'editProjectModal',
            crudUrl: 'project/',
            isUpdateData: true,
            initDataKey: 'projects',
            requiredFields: {
                title: '#projectTitle',
                description: '#projectDescription',
                instructions: '#projectInstructions',
                // Add on mounted
                functionId: null,
                skillIds: null,
                skillLevelBits: null
            },
            mediaFields: ['image', 'files'],
            newFileUniqueIdx: 0
        }
    },
    computed: {
        allowImageToggle() {
            return _.isString(this.formData.image) || _.isString(this.formData.oldImage);
        },
        isImageUpload() {
            return !this.formData.image || !_.isString(this.formData.image);
        },
        projectFunctionsCfg() {
            return {
                maxItems: 1,
                options: _.sortBy(this.initData.functions.map((f) => ({value: f.id, text: f.functionName})), ['text'])
            };
        },
        projectSkillsCfg() {
            return {
                plugins: ['remove_button'],
                maxItems: null,
                options: _.sortBy(this.initData.skills.map((s) => ({value: s.id, text: s.skillName})), ['text'])
            };
        },
        projectSkillLevelsCfg() {
            return {
                plugins: ['remove_button'],
                maxItems: null,
                options: Object.entries(this.globalData.SKILL_LEVEL).map(([key, txt]) => ({value: key, text: txt}))
            }
        }
    },
    methods: {
        addFileInput() {
            const formId = `new-${this.newFileUniqueIdx}`
            this.formData.newFiles[formId] = {
                file: null,
                title: null,
                description: null,
                isShowUpload: true,
                formId
            };
            this.newFileUniqueIdx += 1;
        },
        changeFile(fileId) {
            const file = this.formData.newFiles[fileId];
            const currentFile = file.file;
            file.file = file.oldFile;
            file.oldFile = currentFile;
            file.isShowUpload = !file.isShowUpload;
        },
        removeFileInput(fileId) {
            delete this.formData.newFiles[fileId];
        },
        toggleImageUpload() {
            const currentImage = this.formData.image;
            this.formData.image = this.formData.oldImage;
            this.formData.oldImage = currentImage;
        },
        processRawData(rawData) {
            // Update employer selectize with data
            this.$refs['projectEmployer'].elSel.addOption((rawData.employers || []).map((e) => ({value: e.id, text: e.companyName})))
            this.$refs['projectEmployer'].elSel.refreshOptions(false);

            this.requiredFields.functionId = this.$refs['projectFunction'].targetEl;
            this.requiredFields.skillIds = this.$refs['projectSkills'].targetEl;
            this.requiredFields.skillLevelBits = this.$refs['projectSkillLevels'].targetEl;

            const formData = rawData.formData;
            if (!formData || _.isEmpty(formData)) {
                return {newFiles: {}};
            }

            const newFiles = formData.files.reduce((newFiles, file) => {
                newFiles[file.id] = Object.assign(file, {
                    isShowUpload: false,
                    formId: file.id
                });
                return newFiles;
            }, {})

            return Object.assign(formData, {newFiles});
        },
        getSkillLevelsFromBits(skillLevelBits) {
            return Object.keys(this.globalData.SKILL_LEVEL).filter((t) => parseInt(t) & skillLevelBits);
        },
        setFormFields() {
            const {skillLevelBits, functionId, skills, employer} = this.formData;
            this.$refs['projectSkillLevels'].elSel.setValue(this.getSkillLevelsFromBits(skillLevelBits));

            // Set other selectize elements
            this.$refs['projectFunction'].elSel.setValue(functionId);
            this.$refs['projectSkills'].elSel.setValue((skills || []).map((s) => s.id));
            this.$refs['projectEmployer'].elSel.setValue((employer) ? employer.id : null);
        },
        processFormData() {
            const formData = this.readForm();
            return Object.assign({},
                _.omit(formData, ['files', 'newFiles']),
                {
                    filesMetaData: Object.values(formData.newFiles).map((file) => {
                        return Object.assign(
                            _.omit(file, 'file'),
                            {fileKey: _.isString(file.file) ? null : file.file.name}
                        )
                    }),
                    files: Object.values(formData.newFiles).map((file) => file.file)
                }
            );
        },
        isGoodFormFields(formData) {
            if (form.isEmptyWysiwyg(formData.description)) {
                this.addPopover($('#projectDescription'),
                {severity: SEVERITY_WARN, content: 'Required field', isOnce: true}
                    );
                return false;
            }
            // Check required fields for each file
            const uniqueFileKeys = [];
            for (let i=0; i<formData.files.length; i++) {
                const fileMetaData = formData.filesMetaData[i];
                if (!formData.files[i]) {
                    this.addPopover($(`#projectFile-file-${fileMetaData.formId}`),
                {severity: severity.WARN, content: 'Required field', isOnce: true}
                    );
                    return false;
                }
                if (!fileMetaData.title) {
                    this.addPopover($(`#projectFile-title-${fileMetaData.formId}`),
                {severity: severity.WARN, content: 'Required field', isOnce: true}
                    );
                    return false;
                }
                if (!fileMetaData.skillLevelBits) {
                    this.addPopover($(`#projectFile-skillBits-${fileMetaData.formId}`),
                {severity: severity.WARN, content: 'Required field', isOnce: true}
                    );
                    return false;
                }
                if (fileMetaData.fileKey && uniqueFileKeys.includes(fileMetaData.fileKey)) {
                    this.addPopover($(`#projectFile-file-${fileMetaData.formId}`),
                {severity: severity.WARN, content: 'File cannot have the same name as another file', isOnce: true}
                    );
                    return false;
                }
                if (fileMetaData.fileKey) {
                    uniqueFileKeys.push(fileMetaData.fileKey);
                }
            }
            return true;
        }
    }
}
</script>