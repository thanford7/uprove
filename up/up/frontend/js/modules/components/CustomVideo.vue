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
        <div>
            <span>
                <button class="btn btn-sm -color-orange" :id="recordBtnId"><i class="fas fa-video"></i> Record video</button>
                &nbsp;<button class="btn btn-sm -color-red" :id="stopBtnId"><i class="fas fa-stop"></i> Stop video</button>
            </span>
        </div>
        <div class="row">
            <video id="live-video" width="320"></video>
            <video id="recorded-video" width="320"></video>
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
            recorder: null,
            liveStream: null
        }
    },
    computed: {
        recordBtnId() {
            return `record-${this.elId}`;
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
            const chunks = [];
            // get video & audio stream from user
            const avStream = await navigator.mediaDevices.getUserMedia({
                audio: {deviceId: this.$refs.audioInput.elSel.getValue()},
                video: {
                    deviceId: this.$refs.videoInput.elSel.getValue(),
                    facingMode: 'user'  // Prefer the front facing camera for mobile devices
                }
            });
            const screenStream = await  navigator.mediaDevices.getDisplayMedia({video: true, audio: false});
            const combinedStream = new MediaStream([...avStream.getTracks(), ...screenStream.getTracks()]);

            this.liveStream = combinedStream;

            const liveVideo$ = $('#live-video');
            liveVideo$.prop('srcObject', combinedStream);
            liveVideo$[0].play();

            this.recordBtn$.prop('disabled', false);
            this.recorder = new MediaRecorder(this.liveStream);
            this.recorder.ondataavailable = (e) => {
                chunks.push(e.data);
            }
            this.recorder.onstop = (e) => {
                const blob = new Blob(chunks, {type: 'video/mp4'});
                const videoOutput$ = $('#recorded-video');
                videoOutput$.prop('src', URL.createObjectURL(blob));
                videoOutput$.prop('controls', true);
            }

            this.recordBtn$.prop('disabled', true);
            this.stopBtn$.prop('disabled', false);

            this.recorder.start();
        },
        stopRecording() {
            this.recordBtn$.prop('disabled', false);
            this.stopBtn$.prop('disabled', true);

            // Stop the recorder
            this.recorder.stop();
            this.recorder = null;

            // Stop the media stream
            this.liveStream.getTracks().forEach((track) => {
                track.stop();
            });
            this.liveStream = null;
            $('#live-video').stop();
        }
    },
    mounted() {
        this.recordBtn$ = $(`#${this.recordBtnId}`);
        this.stopBtn$ = $(`#${this.stopBtnId}`);
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