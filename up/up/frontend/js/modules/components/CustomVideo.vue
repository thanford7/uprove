<template>
    <template v-if="isSupported">
        <div class="row">
            <div class="col-md-5">
                <h6>Audio capture device</h6>
                <InputSelectize ref="audioInput" :elId="getNewElUid()" :cfg="{maxItems: 1, valueField: 'deviceId', labelField: 'label'}"/>
            </div>
        </div>
        <div class="row">
            <div class="col-md-5">
                <h6>Video capture device</h6>
                <InputSelectize ref="videoInput" :elId="getNewElUid()" :cfg="{maxItems: 1, valueField: 'deviceId', labelField: 'label'}"/>
            </div>
        </div>
        <div class="row mb-3">
            <span>
                <button class="btn btn-sm -color-orange" :id="recordBtnId"><i class="fas fa-video"></i> Record video</button>
                &nbsp;<button class="btn btn-sm -color-red" :id="stopBtnId"><i class="fas fa-stop"></i> Stop video</button>
                &nbsp;<button class="btn btn-sm btn-primary" :id="saveBtnId" hidden><i class="fas fa-save"></i> Save video</button>
            </span>
        </div>
        <div class="row">
            <div class="col-md-5">
                <video id="live-video" muted height="300"></video>
            </div>
            <div class="col-md-5">
                <video id="live-screen" muted height="300"></video>
            </div>
        </div>
    </template>
</template>

<script>
import InputSelectize from "../inputs/InputSelectize";
export default {
    name: "CustomVideo",
    props: ['elId'],
    components: {InputSelectize},
    data() {
        return {
            recordBtn$: null,
            stopBtn$: null,
            saveBtn$: null,
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
        isSupported() {
            return Boolean(navigator?.mediaDevices?.getUserMedia);
        }
    },
    methods: {
        async startRecording() {
            const avChunks = [];
            const screenChunks = [];
            // get video & audio stream from user
            const avStream = await navigator.mediaDevices.getUserMedia({
                audio: {deviceId: this.$refs.audioInput.elSel.getValue()},
                video: {
                    deviceId: this.$refs.videoInput.elSel.getValue(),
                    facingMode: 'user'  // Prefer the front facing camera for mobile devices
                }
            });
            const screenStream = await  navigator.mediaDevices.getDisplayMedia({
                video: {cursor: 'always'},
                audio: false
            });

            this.liveAvStream = avStream;
            this.liveScreenStream = screenStream;

            this.recordBtn$.prop('disabled', false);
            [
                ['avRecorder', 'liveAvStream', avChunks, $('#live-video')],
                ['screenRecorder', 'liveScreenStream', screenChunks, $('#live-screen')]
            ].forEach(([recorderStr, streamStr, chunks, video$]) => {
                const stream = this[streamStr];
                // Start showing the video feed on the screen
                video$.prop('src', null);
                video$.prop('controls', false);
                video$.prop('muted', true);
                video$.prop('srcObject', stream);
                video$[0].play();

                // Create video recorder
                this[recorderStr] = new MediaRecorder(stream);
                this[recorderStr].ondataavailable = (e) => {
                    chunks.push(e.data);
                }

                // Show the recorded video with playback options
                this[recorderStr].onstop = (e) => {
                    const blob = new Blob(chunks, {type: 'video/mp4'});
                    video$.prop('srcObject', null);  // Remove the live stream
                    video$.prop('src', URL.createObjectURL(blob));  // Add the recorded video
                    video$.prop('controls', true);
                    video$.prop('muted', false);

                    // TODO: Allow user to delete or save video at this point
                }

                // Start recording the video feed
                this[recorderStr].start();
            })

            this.recordBtn$.prop('disabled', true);
            this.stopBtn$.prop('disabled', false);
            this.saveBtn$.prop('hidden', true);
        },
        stopRecording() {
            this.recordBtn$.prop('disabled', false);
            this.stopBtn$.prop('disabled', true);
            this.saveBtn$.prop('hidden', false);

            [
                ['avRecorder', 'liveAvStream', $('#live-video')],
                ['screenRecorder', 'liveScreenStream', $('#live-screen')]
            ].forEach(([recorderStr, streamStr, video$]) => {
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
    }
}
</script>