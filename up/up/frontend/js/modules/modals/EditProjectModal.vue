<template>
    <BaseModal
        :modalId="modalName"
        :modalTitle="(formData.id) ? `Edit project: ${formData.title} (${formData.id})`: 'Create new project'"
        :primaryButtonText="(formData.id) ? 'Save changes' : 'Create project'"
        :isAllowDelete="Boolean(formData.id)"
        :isLargeDisplay="true"
        :isScrollable="true"
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
            <label for="role" class="form-label">Role</label>
            <InputSelectize
                ref="role"
                elId="role"
                :isParseAsInt="true"
                placeholder="Required" :cfg="rolesCfg" @selected="formData.roleId = $event"
            />
        </div>
        <div class="mb-3">
            <label class="form-label">Skills</label>
            <EditSkillsTable ref="skillsTable" :skills="formData.skills"/>
        </div>
        <div class="mb-3">
            <label for="projectSkillLevels" class="form-label">Skill levels</label>
            <SkillLevelsSelectize
                ref="projectSkillLevels"
                placeholder="Required"
                @selected="setProjectSkillLevelBits"
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
            <label class="form-label">Background</label>
            <InputWsiwyg
                elId="projectBackground"
                placeholder="Add background..."
                v-model="formData.background"
            />
        </div>
        <div class="mb-3">
            <label class="form-label">Instructions</label>
            <InputWsiwyg
                elId="`projectInstructions"
                placeholder="Add instructions..."
                v-model="formData.instructions"
            />
        </div>
        <div class="mb-3">
            <label class="form-label">Evaluation criteria</label>
            <div v-for="criterion in formData.evaluationCriteria" class="mb-3 pt-1 -hover-highlight-border position-relative">
                <InputSelectize
                    :ref="`projectCriterion-category-${criterion.id}`"
                    :elId="`projectCriterion-category-${criterion.id}`"
                    :items="criterion.category"
                    placeholder="Category (optional)" :cfg="projectEvaluationCriteriaCategoryCfg" @selected="setEvaluationCategoryAndUpdateOptions(criterion, $event)"
                />
                <textarea
                    rows="2" class="form-control"
                    placeholder="Criterion..."
                    :id="`projectCriterion-criterion-${criterion.id}`"
                    v-model="criterion.criterion"
                />
                <RemoveIcon @click="removeCriterionInput(criterion)"/>
            </div>
            <div class="pt-1">
                <a href="#" @click="addCriterionInput"><i class="fas fa-plus -color-green-text"></i> Add evaluation criterion</a>
            </div>
        </div>
        <div class="mb-3 pt-1 border-top -hover-highlight-border position-relative" v-for="(file, fileId, idx) in formData.newFiles">
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
            <SkillLevelsSelectize
                :ref="`projectFile-skillBits-${fileId}`"
                :items="getSkillLevelNumbersFromBits(file.skillLevelBits)"
                placeholder="Required"
                @selected="file.skillLevelBits = $event"
            />
            <a v-if="file.oldFile || file.id" href="#" @click="changeFile(fileId)">
                <i class="fas fa-exchange-alt"></i>
                &nbsp;{{(file.isShowUpload) ? 'Use existing file' : 'Change file'}}
            </a>
            <RemoveIcon @click="removeFileInput(fileId)"/>
        </div>
        <div class="border-top pt-1">
            <a href="#" @click="addFileInput"><i class="fas fa-plus -color-green-text"></i> Add new file</a>
        </div>
    </BaseModal>
</template>

<script>
import {SEVERITY} from '../../globalData';
import BaseModal from "./BaseModal";
import dataUtil from "../../utils/data";
import EditSkillsTable from "../components/EditSkillsTable";
import FileDisplay from "../components/FileDisplay";
import FormChecker from '../../utils/form';
import InputMedia from "../inputs/InputMedia";
import InputSelectize from "../inputs/InputSelectize";
import InputWsiwyg from "../inputs/InputWsiwyg";
import RemoveIcon from "../components/RemoveIcon";
import skillLevelSelectize from "../selectizeCfgs/skillLevels";
import SkillLevelsSelectize from "../inputs/SkillLevelsSelectize";
import form from "../../utils/form";
import $ from "jquery";

export default {
    name: "EditProjectModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    components: {
        BaseModal, EditSkillsTable, FileDisplay, InputMedia, InputSelectize,
        InputWsiwyg, RemoveIcon, SkillLevelsSelectize
    },
    data() {
        return {
            modalName: 'editProjectModal',
            crudUrl: 'project/',
            isHardRefresh: true,
            requiredFields: {
                title: '#projectTitle',
                description: '#projectDescription',
                background: '#projectBackground',
                // Add on mounted
                roleId: null,
                skillLevelBits: null
            },
            mediaFields: new Set(['image', 'files']),
            newFileUniqueIdx: 0,
            newCriterionUniqueIdx: 0
        }
    },
    computed: {
        allowImageToggle() {
            return dataUtil.isString(this.formData.image) || dataUtil.isString(this.formData.oldImage);
        },
        isImageUpload() {
            return !this.formData.image || !dataUtil.isString(this.formData.image);
        },
        projectEvaluationCriteriaCategoryCfg() {
            const uniqueCategories = dataUtil.uniqBy(this.formData.evaluationCriteria, 'category');
            return {
                maxItems: 1,
                create: (text) => ({value: text, text}),
                options: dataUtil.sortBy(uniqueCategories.map((c) => ({value: c.category, text: c.category})), 'text')
            };
        },
        rolesCfg() {
            return {
                maxItems: 1,
                options: dataUtil.sortBy(this.initData.roles.map((r) => ({value: r.id, text: r.name})), 'text')
            };
        },
    },
    methods: {
        addCriterionInput() {
            this.formData.evaluationCriteria.push({
                id: `new-${this.newCriterionUniqueIdx}`,
                skillLevelBits: null,
                category: null,
                criterion: null
            });
            this.newCriterionUniqueIdx++;
        },
        removeCriterionInput(criterion) {
            this.formData.evaluationCriteria = this.formData.evaluationCriteria.filter((ec) => ec.id !== criterion.id);
        },
        addFileInput() {
            const formId = `new-${this.newFileUniqueIdx}`
            this.formData.newFiles[formId] = {
                file: null,
                title: null,
                description: null,
                isShowUpload: true,
                formId
            };
            this.newFileUniqueIdx++;
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
        setProjectSkillLevelBits(skillLevelBits) {
            this.formData.skillLevelBits = skillLevelBits;
        },
        setEvaluationCategoryAndUpdateOptions(criterion, category) {
            criterion.category = category;
            Object.entries(this.$refs).forEach(([key, ref]) => {
                if (!key.includes('projectCriterion-category')) {
                    return;
                }
                ref.elSel.addOption({value: category, text: category});
                ref.elSel.refreshOptions(false);
            });
        },
        toggleImageUpload() {
            const currentImage = this.formData.image;
            this.formData.image = this.formData.oldImage;
            this.formData.oldImage = currentImage;
        },
        processRawData(rawData) {
            // Update employer selectize with data
            this.$refs.projectEmployer.elSel.addOption((rawData.employers || []).map((e) => ({value: e.id, text: e.companyName})))
            this.$refs.projectEmployer.elSel.refreshOptions(false);

            this.requiredFields.roleId = this.$refs.role.targetEl;
            this.requiredFields.skillLevelBits = this.$refs.projectSkillLevels.targetEl;

            const formData = rawData.formData;
            if (!formData || dataUtil.isEmpty(formData)) {
                return {newFiles: {}, newInstructions: {}, evaluationCriteria: []};
            }

            const newFiles = formData.files.reduce((newFiles, file) => {
                newFiles[file.id] = Object.assign(file, {
                    isShowUpload: false,
                    formId: file.id
                });
                return newFiles;
            }, {});

            return Object.assign(formData, {newFiles});
        },
        getEmptyFormData() {
            this.$refs.skillsTable.clearData();
            return {};
        },
        setFormFields() {
            const {skillLevelBits, roleId, skills, employer} = this.formData;
            this.$refs.projectSkillLevels.elSel.setValue(this.getSkillLevelNumbersFromBits(skillLevelBits));

            // Set other selectize elements
            this.$refs.role.elSel.setValue(roleId);
            this.$refs.projectEmployer.elSel.setValue((employer) ? employer.id : null);
        },
        processFormData() {
            const formData = this.readForm();
            const skills = this.$refs.skillsTable.getSkills();
            return Object.assign({},
                dataUtil.omit(formData, ['files', 'newFiles', 'skills']),
                {skills},
                dataUtil.getFileFormatForAjaxRequest(formData.newFiles, 'filesMetaData', 'files', 'file')
            );
        },
        isGoodFormFields(formData) {
            if (form.isEmptyWysiwyg(formData.description)) {
                this.addPopover($('#projectDescription'),
                {severity: SEVERITY.WARN, content: 'Required field', isOnce: true}
                    );
                return false;
            }
            // Check required fields for each file
            const uniqueFileKeys = [];
            for (let i=0; i<formData.files.length; i++) {
                const fileMetaData = formData.filesMetaData[i];
                if (!formData.files[i]) {
                    this.addPopover($(`#projectFile-file-${fileMetaData.formId}`),
                {severity: SEVERITY.WARN, content: 'Required field', isOnce: true}
                    );
                    return false;
                }
                if (!fileMetaData.title) {
                    this.addPopover($(`#projectFile-title-${fileMetaData.formId}`),
                {severity: SEVERITY.WARN, content: 'Required field', isOnce: true}
                    );
                    return false;
                }
                if (!fileMetaData.skillLevelBits) {
                    const targetEl = this.$refs[`projectFile-skillBits-${fileMetaData.formId}`].targetEl;
                    this.addPopover($(targetEl),
                {severity: SEVERITY.WARN, content: 'Required field', isOnce: true}
                    );
                    return false;
                }
                if (fileMetaData.fileKey && uniqueFileKeys.includes(fileMetaData.fileKey)) {
                    this.addPopover($(`#projectFile-file-${fileMetaData.formId}`),
                {severity: SEVERITY.WARN, content: 'File cannot have the same name as another file', isOnce: true}
                    );
                    return false;
                }
                if (fileMetaData.fileKey) {
                    uniqueFileKeys.push(fileMetaData.fileKey);
                }
            }

             for (let i=0; i<formData.evaluationCriteria.length; i++) {
                 const criterion = formData.evaluationCriteria[i];
                 if (!criterion.criterion) {
                     this.addPopover($(`#projectCriterion-criterion-${criterion.id}`),
                {severity: SEVERITY.WARN, content: 'Criterion is required', isOnce: true}
                    );
                    return false;
                 }
             }

            return true;
        }
    }
}
</script>