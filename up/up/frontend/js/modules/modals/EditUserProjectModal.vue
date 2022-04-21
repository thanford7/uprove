<template>
    <BaseModal
        :modalId="modalName"
        :modalTitle="(formData.id) ? `Edit project: ${formData.customProject.projectTitle}`: 'Create new project'"
        :isAllowDelete="Boolean(formData.id)"
        :isLargeDisplay="true"
    >
        <div class="mb-3 -border-bottom--light">
            <div class="d-flex align-items-center">
                <h6 class="-text-bold m-0" style="display: inline-block;">Files</h6>&nbsp;
                <span v-if="formData.files" class="badge rounded-pill bg-secondary">{{formData.files.length}}</span>
            </div>
            <div v-for="(file, idx) in formData.files" class="-hover-highlight-border mb-2 position-relative">
                <input :id="`file-title-${file.id}`" type="text" class="form-control mb-2" placeholder="File name" v-model="file.title">
                <div v-if="!isNew(file.id)">
                    <a :href="file.file" download>
                        <i class="fas fa-download"></i> {{getFileName(file.file)}}
                    </a>
                </div>
                <InputSelectOrUploadMedia v-else
                    :mediaTypes="[contentTypes.FILE]"
                    assetsKey="user"
                    @selectedMediaNew="file.file = $event"
                    @selectedMediaExisting="replaceFile($event, idx, 'files')"
                />
                <RemoveIcon @click="removeFile(file.id)"/>
            </div>
            <div class="mb-1">
                <AddNewLink :clickFn="addNewFile" text="Add new file"/>
            </div>
        </div>
        <div class="mb-3 -border-bottom--light">
            <div class="d-flex align-items-center">
                <h6 class="-text-bold m-0" style="display: inline-block;">Videos</h6>&nbsp;
                <span v-if="formData.videos" class="badge rounded-pill bg-secondary">{{formData.videos.length}}</span>
            </div>
            <div v-for="(video, idx) in formData.videos" class="-hover-highlight-border mb-2 position-relative">
                <input :id="`video-title-${video.id}`" type="text" class="form-control mb-2" placeholder="Video name" v-model="video.title">
                <div v-if="!isNew(video.id)">
                    <a :href="video.video" download>
                        <i class="fas fa-download"></i> {{getFileName(video.video)}}
                    </a>
                </div>
                <InputSelectOrUploadMedia v-else
                    :mediaTypes="[contentTypes.VIDEO]"
                    assetsKey="user"
                    @selectedMediaNew="video.video = $event"
                    @selectedMediaExisting="replaceFile($event, idx, 'videos')"
                />
                <RemoveIcon @click="removeVideo(video.id)"/>
            </div>
            <div class="mb-1">
                <AddNewLink :clickFn="addNewVideo" text="Add new video file"/>
                <span v-if="isVideoCaptureSupported">
                    &nbsp;
                    <a href="#"
                       @click="eventBus.emit('open:addVideoRecordingModal', formData)"
                       data-bs-dismiss="modal"
                       class="-color-green-text"
                    >
                        <i class="fas fa-video"></i>
                        &nbsp;Record a new video
                    </a>
                </span>
            </div>
        </div>
        <div class="mb-3 -border-bottom--light">
            <div class="d-flex align-items-center">
                <h6 class="-text-bold m-0" style="display: inline-block;">Images</h6>&nbsp;
                <span v-if="formData.images" class="badge rounded-pill bg-secondary">{{formData.images.length}}</span>
            </div>
            <div v-for="(image, idx) in formData.images" class="-hover-highlight-border mb-2 position-relative">
                <input :id="`image-title-${image.id}`" type="text" class="form-control mb-2" placeholder="Image name" v-model="image.title">
                <div v-if="!isNew(image.id)">
                    <a :href="image.image" download>
                        <i class="fas fa-download"></i> {{getFileName(image.image)}}
                    </a>
                </div>
                <InputSelectOrUploadMedia v-else
                    :mediaTypes="[contentTypes.IMAGE]"
                    assetsKey="user"
                    @selectedMediaNew="image.image = $event"
                    @selectedMediaExisting="replaceFile($event, idx, 'images')"
                />
                <RemoveIcon @click="removeImage(image.id)"/>
            </div>
            <div class="mb-1">
                <AddNewLink :clickFn="addNewImage" text="Add new image file"/>
            </div>
        </div>
        <div class="mb-3">
            <h6 class="-text-bold">Project Notes <InfoToolTip :elId="getNewElUid()" :content="TOOLTIPS.userProjectNotes"/></h6>
            <InputWsiwyg v-model="formData.projectNotes" elId="blogPost" placeholder="Write post..."/>
        </div>
        <template v-slot:footer>
            <ButtonDelete class="-pull-left" @click="deleteObject"/>
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button
                @click="saveChange"
                type="button" class="btn btn-primary"
                :disabled="formData.isLocked"
                :title="getProjectLockedNote(formData)"
            >
                <span v-if="formData.isLocked"><i class="fas fa-lock"></i>&nbsp;</span>
                {{(formData.id) ? 'Save changes' : 'Create project'}}
            </button>
        </template>
    </BaseModal>
</template>

<script>
import {CONTENT_TYPES, SEVERITY} from '../../globalData';
import AddNewLink from "../components/AddNewLink";
import BaseModal from "./BaseModal";
import dataUtil from "../../utils/data";
import InfoToolTip from "../components/InfoToolTip";
import InputSelectOrUploadMedia from "../inputs/InputSelectOrUploadMedia";
import InputWsiwyg from "../inputs/InputWsiwyg";
import RemoveIcon from "../components/RemoveIcon";
import userProjectUtil from "../../utils/userProject";
import $ from "jquery";

export default {
    name: "EditUserProjectModal",
    extends: BaseModal,
    inheritAttrs: false,
    components: {AddNewLink, BaseModal, InfoToolTip, InputSelectOrUploadMedia, InputWsiwyg, RemoveIcon},
    data() {
        return {
            modalName: 'editUserProjectModal',
            crudUrl: 'user-project/',
            isUpdateData: true,
            initDataKey: 'userProjects',
            newFileCount: 0,
            newVideoCount: 0,
            newImageCount: 0,
            mediaFields: new Set(['file', 'video', 'image']),
            contentTypes: CONTENT_TYPES
        }
    },
    computed: {
        isVideoCaptureSupported() {
            return Boolean(navigator?.mediaDevices?.getUserMedia);
        }
    },
    methods: {
        getProjectLockedNote: userProjectUtil.getProjectLockedNote,
        addNewFile() {
            this.newFileCount++;
            this.formData.files.push({
                id: `new-${this.newFileCount}`
            });
        },
        removeFile(id) {
            this.formData.files = this.formData.files.filter((file) => file.id !== id);
        },
        replaceFile({id}, idx, type) {
            const assets = this.initData.user[type];
            this.formData[type][idx] = assets.find((a) => a.id === parseInt(id));
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
            return Object.assign(
                dataUtil.omit(formData, ['files', 'videos', 'images']),
                dataUtil.getFileFormatForAjaxRequest(formData.files, 'filesMetaData', 'file', 'file'),
                dataUtil.getFileFormatForAjaxRequest(formData.videos, 'videosMetaData', 'video', 'video'),
                dataUtil.getFileFormatForAjaxRequest(formData.images, 'imagesMetaData', 'image', 'image'),
            );
        },
        isGoodFormFields(formData) {
            const checkFields = [
                {dataKey: 'file', metaDataKey: 'filesMetaData', idKey: 'file'},
                {dataKey: 'video', metaDataKey: 'videosMetaData', idKey: 'video'},
                {dataKey: 'image', metaDataKey: 'imagesMetaData', idKey: 'image'},
            ];

            for (let x = 0; x < checkFields.length; x++) {
                const {dataKey, metaDataKey, idKey} = checkFields[x];
                const uniqueFileKeys = [];
                for (let i = 0; i < formData[dataKey].length; i++) {
                    const file = formData[dataKey][i];
                    const metaData = formData[metaDataKey][i];
                    // Only new files will have a fileKey. We don't need to worry about name collisions from previous files
                    if (metaData.fileKey) {
                        if (uniqueFileKeys.includes(metaData.fileKey)) {
                            this.addPopover($(`#${idKey}-input-${metaData.id}`),
                            {severity: SEVERITY.WARN, content: 'File name must be unique', isOnce: true}
                                );
                            return false;
                        }
                        uniqueFileKeys.push(metaData.fileKey);
                    }
                    if (!file) {
                        this.addPopover($(`#${idKey}-input-${metaData.id}`),
                        {severity: SEVERITY.WARN, content: 'Required field', isOnce: true}
                            );
                        return false;
                    }
                    if (!metaData.title) {
                        this.addPopover($(`#${idKey}-title-${metaData.id}`),
                    {severity: SEVERITY.WARN, content: 'Required field', isOnce: true}
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