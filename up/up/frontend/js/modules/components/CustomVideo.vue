<template>
    <div>
        <div v-if="isUserAllowedInput">
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
                <button class="btn btn-sm -color-orange -color-hover-white-text"
                        :id="recordBtnId"
                >
                    <i class="fas fa-video"></i> Record video
                </button>&nbsp;
                <button class="btn btn-sm -color-red -color-hover-white-text"
                         :id="stopBtnId"
                >
                    <i class="fas fa-stop"></i> Stop video
                </button>&nbsp;
                <button class="btn btn-sm btn-primary"
                        :id="saveBtnId" hidden
                        @click="saveChangeWithBanner"
                >
                    <i class="fas fa-save"></i> Save video
                </button>
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
    </div>
        <div v-else>
            You must allow video and audio input to record a video. Click the button below to update access permissions.
            <button class="btn btn-secondary" @click="setMediaDevices">
                Request access
            </button>
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
            isUserAllowedInput: true,  // Need to check whether use has allowed camera and audio capture
            isMediaError: false,
            recordingStartSeconds: null,
            recordBtn$: null,
            stopBtn$: null,
            saveBtn$: null,
            hasData: false,
            avRecorder: null,
            liveAvStream: null,
            screenRecorder: null,
            liveScreenStream: null,
            audioRecorder: null,
            liveAudioStream: null
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
        addMediaError(mediaType) {
            this.isMediaError = true;
            const message = `Something is preventing media capture for the ${mediaType}. Please make sure no other
            applications are running screen share or video share and try again. If the problem persists, try quiting and
            reopening your web browser.`
            store.commit('addAlert', {
                message,
                alertType: SEVERITY.DANGER
            });
        },
        afterUpdateInitData(newVideo) {
            if (this.isUpdateProject) {
                // Update the formData if the user hasn't navigated away from this modal
                this.$emit('videoComplete', newVideo);

                // Update the formData if the user has navigated away from this modal
                this.eventBus.emit('injectFormData', [
                    'editUserProjectModal',
                    (target) => { target.push(newVideo); },
                    'videos'
                ]);
            }
        },
        getSuccessMessage(video) {
            return `Video processing complete for ${video.title}`;
        },
        processFormData() {
            return Object.assign(this.readForm(), this.addFormData || {});
        },
        saveChangeWithBanner(val) {
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
            this.saveChange(val);
        },
        setAjaxUpdate() {
            this.initDataKey = this.targetInitDataKey;
            this.isUpdateData = Boolean(this.initDataKey);
        },
        async startRecording() {
            this.isMediaError = false;
            const recorders = [];
            this.hasData = true;

            if (this.recordingType !== this.TYPE_SCREEN) {
                // get video & audio stream from user
                const avChunks = [];
                try {
                    this.liveAvStream = await navigator.mediaDevices.getUserMedia({
                        audio: {deviceId: this.$refs.audioInput.elSel.getValue()},
                        video: {
                            deviceId: this.$refs.videoInput.elSel.getValue(),
                            facingMode: 'user'  // Prefer the front facing camera for mobile devices
                        }
                    });
                } catch (e) {
                    this.addMediaError('video');
                }

                recorders.push({
                    recorderStr: 'avRecorder',
                    streamStr: 'liveAvStream',
                    chunks: avChunks,
                    video$: $('#live-video'),
                    formField: 'avVideo',
                });
            }

            if (this.recordingType !== this.TYPE_VIDEO) {
                const screenChunks = [];
                try {
                    this.liveScreenStream = await navigator.mediaDevices.getDisplayMedia({
                        video: {cursor: 'always'},
                        audio: false
                    });
                } catch (e) {
                    this.addMediaError('screen');
                }

                // getDisplayMedia does not support audio capture for most browsers (and only PC)
                // If we are only recording screen capture, we need to create an additional stream for the audio
                if (this.recordingType === TYPE_SCREEN) {
                    try {
                        this.liveAudioStream = await navigator.mediaDevices.getUserMedia({
                            audio: {deviceId: this.$refs.audioInput.elSel.getValue()},
                            video: false
                        });
                    } catch (e) {
                        this.addMediaError('audio');
                    }
                }

                recorders.push({
                    recorderStr: 'screenRecorder',
                    streamStr: 'liveScreenStream',
                    chunks: screenChunks,
                    video$: $('#live-screen'),
                    formField: 'screenVideo',
                    audioStreamStr: 'liveAudioStream'
                });
            }

            if (this.isMediaError) {
                this.stopRecording();
                return;
            }

            // Pause to allow the user to get ready to record
            this.recordingStartSeconds = RECORDING_WAIT_SECONDS;
            for (let i = 1; i <= RECORDING_WAIT_SECONDS; i++) {
                setTimeout(() => {
                    // If user stops recording before the end of countdown, we don't want to continue to decrement
                    if (this.recordingStartSeconds > 0) {
                        this.recordingStartSeconds--;
                    }
                }, i * 1000);
            }

            setTimeout(() => {
                this.recordBtn$.prop('disabled', false);
                recorders.forEach(({recorderStr, streamStr, chunks, video$, formField, audioStreamStr}) => {
                    let stream = this[streamStr];
                    const audioStream = this[audioStreamStr];
                    if (audioStream) {
                        stream = new MediaStream([...stream.getVideoTracks(), ...audioStream.getAudioTracks()]);
                    }

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
            this.recordingStartSeconds = 0;
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
        },
        async setMediaDevices() {
            const devices = await this.getMediaAccess();
            if (!devices) {
                return;
            }

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
        },
        async getMediaAccess() {
            let devices = await navigator.mediaDevices.enumerateDevices();
            const getIsAccessAllowed = (devices) => {
                return devices.reduce((isAllowed, {deviceId}) => {
                    isAllowed = isAllowed || (deviceId && deviceId.length);
                    return isAllowed;
                }, false);
            }
            let isAccessAllowed = getIsAccessAllowed(devices);

            // If user hasn't granted permission to use computer devices we can request access using getUserMedia
            if (!isAccessAllowed) {
                await navigator.mediaDevices.getUserMedia({audio: true, video: true});
                devices = await navigator.mediaDevices.enumerateDevices();
                isAccessAllowed = getIsAccessAllowed(devices);
            }
            this.isUserAllowedInput = isAccessAllowed;
            return (isAccessAllowed) ? devices : null;
        }
    },
    mounted() {
        this.setAjaxUpdate()
        this.recordBtn$ = $(`#${this.recordBtnId}`);
        this.stopBtn$ = $(`#${this.stopBtnId}`);
        this.saveBtn$ = $(`#${this.saveBtnId}`);
        this.recordBtn$.on('click', this.startRecording);
        this.stopBtn$.on('click', this.stopRecording);
    },
    updated() {
        this.setAjaxUpdate();
    }
}
</script>