<template>
    <a v-if="isLink" :id="elId" href="#" class="-color-green-text">
        <i class="fas fa-video"></i> Record video
    </a>
    <button v-else class="btn btn-sm -color-orange" :id="elId"><i class="fas fa-video"></i> Record video</button>
    <div v-html="embedPlayerHtml"/>
</template>

<script>
import {isSupported, setup} from "@loomhq/loom-sdk";
import {oembed} from "@loomhq/loom-embed";

export default {
    name: "LoomVideo",
    props: ['elId', 'isLink'],
    data() {
        return {
            embedPlayerHtml: null
        }
    },
    async mounted() {
        const {supported, error} = await isSupported();

        if (!supported) {
            console.warn(`Error setting up Loom: ${error}`);
            return;
        }

        const button = document.getElementById(this.elId);

        if (!button) {
            console.log('Error: No button');
            return;
        }

        const {configureButton} = await setup({
            publicAppId: this.globalData.LOOM_API_KEY
        });

        const sdkButton = configureButton({element: button});

        sdkButton.on('insert-click', async (video) => {
            const {html} = await oembed(video.sharedUrl, {width: 400});
            this.embedPlayerHtml = html;
        });
    }
}
</script>