<template>
    <div class="row">
        <div class="col">
            <h6 style="display: inline-block;">Recording type</h6>&nbsp;
            <InfoToolTip :elId="getNewElUid()" :isHtmlContent="true" content="
                <p>All content types will record audio. Differences between options are:</p>
                <ul>
                    <li>
                        <code>Screen and video</code>: Records a screen, application, or browser tab while simultaneously
                        recording a user facing video. After saving, the two videos will be combined into a single video with
                        the two videos playing side by side. This option is ideal if you are showing a presentation and want
                        to record yourself as well.
                    </li>
                    <li>
                        <code>Video</code>: Records a user facing video. This option is ideal if you are recording yourself
                        answering a question or discussing a project, but don't have any files to present.
                    </li>
                    <li>
                        <code>Screen</code>: Records a user facing video. This option is ideal if you are recording yourself
                        answering a question or discussing a project, but don't have any files to present.
                    </li>
                </ul>
            "
            />
            <InputSelectize
                ref="recordingType"
                :elId="getNewElUid()"
                :cfg="recordingTypeCfg"
                :isPreserveValue="true"
                @selected="recordingType = $event"
            />
        </div>
    </div>
    <div class="row">
        <div class="col">
            <h6>Audio capture device</h6>
            <InputSelectize
                ref="audioInput"
                :elId="getNewElUid()"
                :cfg="{maxItems: 1, valueField: 'deviceId', labelField: 'label'}"
                :isPreserveValue="true"
            />
        </div>
    </div>
    <div class="row" :style="(recordingType !== TYPE_SCREEN) ? 'display: auto;' : 'display: none;'">
        <div class="col">
            <h6>Video capture device</h6>
            <InputSelectize
                ref="videoInput"
                :elId="getNewElUid()"
                :cfg="{maxItems: 1, valueField: 'deviceId', labelField: 'label'}"
                :isPreserveValue="true"
            />
        </div>
    </div>
    <div class="row mb-3">
        <span>
            <button class="btn btn-sm -color-orange" :id="recordBtnId"><i class="fas fa-video"></i> Record video</button>
            &nbsp;<button class="btn btn-sm -color-red" :id="stopBtnId"><i class="fas fa-stop"></i> Stop video</button>
            &nbsp;<button class="btn btn-sm btn-primary" :id="saveBtnId" hidden @click="saveChangeWithBanner"><i class="fas fa-save"></i> Save video</button>
        </span>
    </div>
    <div class="row">
            <h4 v-if="recordingStartSeconds"
                class="-color-white-text -color-darkblue -border-rounded"
            >
                Recording will start in {{pluralize('second', recordingStartSeconds)}}
            </h4>
        <div v-if="hasData" class="mb-2">
            <h6>Video title</h6>
            <input type="text" class="form-control" placeholder="Add a video title" v-model="formData.title">
        </div>
        <p v-if="recordingType === TYPE_SCREEN_VIDEO" class="-sub-text">
            The video feed and screen feed will be combined into one video during post-processing (after you save the videos).
        </p>
        <div v-if="recordingType !== TYPE_SCREEN" :class="(isModal) ? 'col-12' : 'col-md-5'">
            <h6>Video recording</h6>
            <div v-if="!hasData" class="-color-moderategrey -color-white-text -border-rounded p2 text-center">
                Recording will begin when you click the "Record video" button
            </div>
            <video id="live-video" muted :height="(hasData) ? 300 : 0"></video>
        </div>
        <div v-if="recordingType !== TYPE_VIDEO" :class="(isModal) ? 'col-12' : 'col-md-5'">
            <h6>Screen recording</h6>
            <div v-if="!hasData"  class="-color-moderategrey -color-white-text -border-rounded p2 text-center">
                Recording will begin when you click the "Record video" button
            </div>
            <video id="live-screen" muted :height="(hasData) ? 300 : 0"></video>
        </div>
    </div>
</template>

<script>
import {SEVERITY} from '../../globalData';
import InputSelectize from "../inputs/InputSelectize";
import InfoToolTip from "./InfoToolTip";
import {store} from "../../vueMixins";

const TYPE_SCREEN_VIDEO = 'SCREEN_VIDEO';
const TYPE_VIDEO = 'VIDEO';
const TYPE_SCREEN = 'SCREEN';

const RECORDING_TYPES = {
    [TYPE_SCREEN_VIDEO]: 'Screen and video',
    [TYPE_VIDEO]: 'Video',
    [TYPE_SCREEN]: 'Screen'
}

const RECORDING_WAIT_SECONDS = 5;

export default {
    name: "CustomVideo",
    props: [
        'elId', 'isModal',
        'addFormData',  // Additional data to be saved with the video data
        'targetInitDataKey',  // The key path used to update in memory data
        'isUpdateProject' // The current list of videos that the new video should be added to after saving
    ],
    components: {InfoToolTip, InputSelectize},
    data() {
        return {
            crudUrl: 'user-video/',
            initDataKey: null,  // Set on update
            isUpdateData: true,
            mediaFields: new Set(['avVideo', 'screenVideo']),
            recordingTypeCfg: {
                maxItems: 1,
                valueField: 'key',
                labelField: 'val',
                items: [TYPE_SCREEN_VIDEO],
                options: Object.entries(RECORDING_TYPES).map(([key, val]) => ({key, val}))
            },
            TYPE_SCREEN_VIDEO,
            TYPE_VIDEO,
            TYPE_SCREEN,
            recordingType: TYPE_SCREEN_VIDEO,
            recordingStartSeconds: null,
            recordBtn$: null,
            stopBtn$: null,
            saveBtn$: null,
            hasData: false,
            avRecorder: null,
            liveAvStream: null,
            screenRecorder: null,
            liveScreenStream: null
        }
    },
    computed: {
        recordBtnId() {
            return `record-${this.elId}`;
        },
        saveBtnId() {
            return `save-${this.elId}`;
        },
        stopBtnId() {
            return `stop-${this.elId}`;
        },
    },
    methods: {
        afterUpdateInitData(newVideo) {
            if (this.isUpdateProject) {
                this.eventBus.emit('injectFormData', [
                    'editUserProjectModal',
                    (target) => { target.push(newVideo); },
                    'videos'
                ]);
            }
        },
        processFormData() {
            return Object.assign(this.readForm(), this.addFormData || {});
        },
        saveChangeWithBanner(val) {
            if (this.recordingType === TYPE_SCREEN_VIDEO) {
                let message = 'This video requires post-processing which can take a few minutes. ' +
                'You can navigate away from this screen and we\'ll send you an email once the video is done processing.'
                if (this.addFormData && 'projectId' in this.addFormData) {
                    const userProject = this.initData.userProjects.find((up) => up.id === this.addFormData.projectId);
                    message += ` The video will be added to your ${userProject.customProject.projectTitle} project automatically.`
                }
                store.commit('addAlert', {
                    message,
                    alertType: SEVERITY.INFO
                });
            }
            this.saveChange(val);
        },
        setAjaxUpdate() {
            this.initDataKey = this.targetInitDataKey;
            this.isUpdateData = Boolean(this.initDataKey);
        },
        async startRecording() {
            const recorders = [];
            this.hasData = true;

            if (this.recordingType !== this.TYPE_SCREEN) {
                // get video & audio stream from user
                const avChunks = [];
                this.liveAvStream = await navigator.mediaDevices.getUserMedia({
                    audio: {deviceId: this.$refs.audioInput.elSel.getValue()},
                    video: {
                        deviceId: this.$refs.videoInput.elSel.getValue(),
                        facingMode: 'user'  // Prefer the front facing camera for mobile devices
                    }
                });
                recorders.push(['avRecorder', 'liveAvStream', avChunks, $('#live-video'), 'avVideo']);
            }

            if (this.recordingType !== this.TYPE_VIDEO) {
                const screenChunks = [];
                this.liveScreenStream = await navigator.mediaDevices.getDisplayMedia({
                    video: {cursor: 'always'},
                    audio: this.recordingType === TYPE_SCREEN
                });
                recorders.push(['screenRecorder', 'liveScreenStream', screenChunks, $('#live-screen'), 'screenVideo']);
            }

            // Pause to allow the user to get ready to record
            this.recordingStartSeconds = RECORDING_WAIT_SECONDS;
            for (let i = 1; i <= RECORDING_WAIT_SECONDS; i++) {
                setTimeout(() => {
                    this.recordingStartSeconds--;
                }, i * 1000);
            }

            setTimeout(() => {
                this.recordBtn$.prop('disabled', false);
                recorders.forEach(([recorderStr, streamStr, chunks, video$, formField]) => {
                    const stream = this[streamStr];
                    // Start showing the video feed on the screen
                    video$.prop('src', null);
                    video$.prop('controls', false);
                    video$.prop('muted', true);
                    video$.prop('srcObject', stream);
                    video$[0].play();

                    // Create video recorder
                    this[recorderStr] = new MediaRecorder(stream, {mimeType: 'video/webm'});
                    this[recorderStr].ondataavailable = (e) => {
                        chunks.push(e.data);
                    }

                    // Show the recorded video with playback options
                    this[recorderStr].onstop = (e) => {
                        const blob = new Blob(chunks, {type: 'video/webm'});
                        this.formData[formField] = blob;
                        video$.prop('srcObject', null);  // Remove the live stream
                        video$.prop('src', URL.createObjectURL(blob));  // Add the recorded video
                        video$.prop('controls', true);
                        video$.prop('muted', false);
                    }

                    // Start recording the video feed
                    this[recorderStr].start();
                });

                this.recordBtn$.prop('disabled', true);
                this.stopBtn$.prop('disabled', false);
                this.saveBtn$.prop('hidden', true);
            }, RECORDING_WAIT_SECONDS * 1000)
        },
        stopRecording() {
            this.recordBtn$.prop('disabled', false);
            this.stopBtn$.prop('disabled', true);
            this.saveBtn$.prop('hidden', false);

            [
                ['avRecorder', 'liveAvStream', $('#live-video')],
                ['screenRecorder', 'liveScreenStream', $('#live-screen')]
            ].forEach(([recorderStr, streamStr, video$]) => {
                // Short circuit if this recorder isn't in use
                if (!this[recorderStr]) {
                    return;
                }
                // Stop the recorder
                this[recorderStr].stop();
                this[recorderStr] = null;

                // Stop the media stream
                this[streamStr].getTracks().forEach((track) => {
                    track.stop();
                });
                this[streamStr] = null;

                video$.stop();
            })
        }
    },
    mounted() {
        this.setAjaxUpdate()
        this.recordBtn$ = $(`#${this.recordBtnId}`);
        this.stopBtn$ = $(`#${this.stopBtnId}`);
        this.saveBtn$ = $(`#${this.saveBtnId}`);
        this.recordBtn$.on('click', this.startRecording);
        this.stopBtn$.on('click', this.stopRecording);
        navigator.mediaDevices.enumerateDevices()
            .then((devices) => {
                const audioInputDevices = [];
                let audioInputDefault, videoInputDefault;
                const videoInputDevices = [];
                devices.forEach(({kind, label, deviceId}) => {
                    if (kind === 'audioinput') {
                        if (deviceId === 'default') {
                            audioInputDefault = label;
                        } else {
                            audioInputDevices.push({deviceId, label});
                        }
                    }
                    if (kind === 'videoinput') {
                        if (deviceId === 'default') {
                            videoInputDefault = label;
                        } else {
                            videoInputDevices.push({deviceId, label});
                        }
                    }
                });

                // Create selectize for audio input
                if (audioInputDevices?.length) {
                    this.$refs.audioInput.elSel.addOption(audioInputDevices);
                    this.$refs.audioInput.elSel.refreshOptions(false);
                    const defaultAudioId = (audioInputDefault) ?
                        audioInputDevices.find((device) => audioInputDefault.includes(device.label))?.deviceId :
                        audioInputDevices[0].deviceId;
                    this.$refs.audioInput.elSel.addItem(defaultAudioId);
                }

                // Create selectize for video input
                if (videoInputDevices?.length) {
                    this.$refs.videoInput.elSel.addOption(videoInputDevices);
                    this.$refs.videoInput.elSel.refreshOptions(false);
                    const defaultVideoId = (videoInputDefault) ?
                        videoInputDevices.find((device) => videoInputDefault.includes(device.label))?.deviceId :
                        videoInputDevices[0].deviceId;
                    this.$refs.videoInput.elSel.addItem(defaultVideoId);
                }
            });
    },
    updated() {
        this.setAjaxUpdate();
    }
}
</script>