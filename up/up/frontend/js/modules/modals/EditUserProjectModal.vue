<template>
    <BaseModal
        :modalId="modalName"
        :modalTitle="(formData.id) ? `Edit project: ${formData.customProject.projectTitle}`: 'Create new project'"
        :primaryButtonText="(formData.id) ? 'Save changes' : 'Create project'"
        :isAllowDelete="Boolean(formData.id)"
        :isLargeDisplay="true"
        @saveChange="saveChange($event)"
        @deleteObject="deleteObject($event)"
    >
        <div class="mb-3 -border-bottom--light">
            <div class="d-flex align-items-center">
                <h5 class="-text-bold m-0" style="display: inline-block;">Files</h5>&nbsp;
                <span v-if="formData.files" class="badge rounded-pill bg-secondary">{{formData.files.length}}</span>
            </div>
            <div v-for="file in formData.files" class="-hover-highlight-border mb-2 position-relative">
                <input :id="`file-title-${file.id}`" type="text" class="form-control mb-2" placeholder="File name" v-model="file.title">
                <div v-if="!isNew(file.id)">
                    <a :href="file.file" download>
                        <i class="fas fa-download"></i> {{getFileName(file.file)}}
                    </a>
                </div>
                <InputMedia v-else
                    :mediaTypes="['file']"
                    :elId="`file-input-${file.id}`"
                    @selected="file.file = $event"
                />
                <RemoveIcon @click="removeFile(file.id)"/>
            </div>
            <div class="mb-1">
                <AddNewLink :clickFn="addNewFile" text="Add new file"/>
            </div>
        </div>
        <div class="mb-3 -border-bottom--light">
            <div class="d-flex align-items-center">
                <h5 class="-text-bold m-0" style="display: inline-block;">Videos</h5>&nbsp;
                <span v-if="formData.videos" class="badge rounded-pill bg-secondary">{{formData.videos.length}}</span>
            </div>
            <div v-for="video in formData.videos" class="-hover-highlight-border mb-2 position-relative">
                <input :id="`video-title-${video.id}`" type="text" class="form-control mb-2" placeholder="Video name" v-model="video.title">
                <div v-if="!isNew(video.id)">
                    <a :href="video.video" download>
                        <i class="fas fa-download"></i> {{getFileName(video.video)}}
                    </a>
                </div>
                <InputMedia v-else
                    :mediaTypes="['video']"
                    :elId="`video-input-${video.id}`"
                    @selected="video.video = $event"
                />
                <RemoveIcon @click="removeVideo(video.id)"/>
            </div>
            <div class="mb-1">
                <AddNewLink :clickFn="addNewVideo" text="Add new video file"/>
            </div>
        </div>
        <div class="mb-3 -border-bottom--light">
            <div class="d-flex align-items-center">
                <h5 class="-text-bold m-0" style="display: inline-block;">Images</h5>&nbsp;
                <span v-if="formData.images" class="badge rounded-pill bg-secondary">{{formData.images.length}}</span>
            </div>
            <div v-for="image in formData.images" class="-hover-highlight-border mb-2 position-relative">
                <input :id="`image-title-${image.id}`" type="text" class="form-control mb-2" placeholder="Image name" v-model="image.title">
                <div v-if="!isNew(image.id)">
                    <a :href="image.image" download>
                        <i class="fas fa-download"></i> {{getFileName(image.image)}}
                    </a>
                </div>
                <InputMedia v-else
                    :ref="`image-input-${image.id}`"
                    :mediaTypes="['image']"
                    :elId="`image-input-${image.id}`"
                    @selected="image.image = $event"
                />
                <RemoveIcon @click="removeImage(image.id)"/>
            </div>
            <div class="mb-1">
                <AddNewLink :clickFn="addNewImage" text="Add new image file"/>
            </div>
        </div>
        <div class="mb-3">
            <h5 class="-text-bold">Project Notes <InfoToolTip :elId="getNewElUid()" :content="TOOLTIPS.userProjectNotes"/></h5>
            <InputWsiwyg v-model="formData.projectNotes" elId="blogPost" placeholder="Write post..."/>
        </div>
    </BaseModal>
</template>

<script>
import {severity} from "../../vueMixins";
import AddNewLink from "../components/AddNewLink";
import BaseModal from "./BaseModal";
import dataUtil from "../../utils/data";
import InfoToolTip from "../components/InfoToolTip";
import InputMedia from "../inputs/InputMedia";
import InputWsiwyg from "../inputs/InputWsiwyg";
import RemoveIcon from "../components/RemoveIcon";
import $ from "jquery";

export default {
    name: "EditUserProjectModal",
    extends: BaseModal,
    inheritAttrs: false,
    components: {AddNewLink, BaseModal, InfoToolTip, InputMedia, InputWsiwyg, RemoveIcon},
    data() {
        return {
            modalName: 'editUserProjectModal',
            crudUrl: 'user-project/',
            isUpdateData: true,
            initDataKey: 'userProjects',
            newFileCount: 0,
            newVideoCount: 0,
            newImageCount: 0,
            mediaFields: ['files', 'videos', 'images']
        }
    },
    methods: {
        addNewFile() {
            this.newFileCount++;
            this.formData.files.push({
                id: `new-${this.newFileCount}`
            });
        },
        removeFile(id) {
            this.formData.files = this.formData.files.filter((file) => file.id !== id);
        },
        addNewVideo() {
            this.newVideoCount++;
            this.formData.videos.push({
                id: `new-${this.newVideoCount}`
            });
        },
        removeVideo(id) {
            this.formData.videos = this.formData.videos.filter((video) => video.id !== id);
        },
        addNewImage() {
            this.newImageCount++;
            this.formData.images.push({
                id: `new-${this.newImageCount}`
            });
        },
        removeImage(id) {
            this.formData.images = this.formData.images.filter((image) => image.id !== id);
        },
        isNew(id) {
            return id.toString().includes('new');
        },
        getFileName(file) {
            return dataUtil.getFileNameFromUrl(file);
        },
        processFormData() {
            const formData = {...this.formData};

            // Update all media files for saving
            Object.assign(
                formData,
                dataUtil.getFileFormatForAjaxRequest(formData.files, 'filesMetaData', 'files', 'file'),
                dataUtil.getFileFormatForAjaxRequest(formData.videos, 'videosMetaData', 'videos', 'video'),
                dataUtil.getFileFormatForAjaxRequest(formData.images, 'imagesMetaData', 'images', 'image'),
            );

            return formData;
        },
        isGoodFormFields(formData) {
            const checkFields = [
                {dataKey: 'files', metaDataKey: 'filesMetaData', idKey: 'file'},
                {dataKey: 'videos', metaDataKey: 'videosMetaData', idKey: 'video'},
                {dataKey: 'images', metaDataKey: 'imagesMetaData', idKey: 'image'},
            ];

            for (let x = 0; x < checkFields.length; x++) {
                const {dataKey, metaDataKey, idKey} = checkFields[x];
                const uniqueFileKeys = [];
                for (let i = 0; i < formData[dataKey].length; i++) {
                    const file = formData[dataKey][i];
                    const metaData = formData[metaDataKey][i];
                    if (uniqueFileKeys.includes(metaData.fileKey)) {
                        this.addPopover($(`#${idKey}-input-${metaData.id}`),
                        {severity: severity.WARN, content: 'File name must be unique', isOnce: true}
                            );
                        return false;
                    }
                    uniqueFileKeys.push(metaData.fileKey);
                    if (!file) {
                        this.addPopover($(`#${idKey}-input-${metaData.id}`),
                        {severity: severity.WARN, content: 'Required field', isOnce: true}
                            );
                        return false;
                    }
                    if (!metaData.title) {
                        this.addPopover($(`#${idKey}-title-${metaData.id}`),
                    {severity: severity.WARN, content: 'Required field', isOnce: true}
                        );
                        return false;
                    }
                }
            }
            return true;
        }
    }
}
</script>