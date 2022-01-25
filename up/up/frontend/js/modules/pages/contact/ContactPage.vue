<template>
    <div class="container-lg">
        <BannerAlert/>
        <div class="row mt-3 mb-3">
            <h2>Contact us</h2>
            <div class="col-md-6 pt-3 call-out-box" :class="(isMobile) ? 'mb-3' : ''">
                <component :is="(isMobile) ? 'h6' : 'h2'">We want you to have a fantastic hiring experience.</component>
                <i class="fas fa-chart-line" :class="(isMobile) ? 'fa-2x' : 'fa-4x'"></i>
                <component :is="(isMobile) ? 'h6' : 'h2'">Connect with one of our project experts to see how we can help.</component>
            </div>
            <div class="col-md-6">
                <SubmitHelpModal ref="submitHelp" :isContentOnly="true"/>
                <button type="submit" class="btn btn-primary" @click="$refs['submitHelp'].saveChange($event)">Send message</button>
            </div>
        </div>
    </div>
</template>

<script>
import BannerAlert from "../../components/BannerAlert";
import SubmitHelpModal from "../../modals/SubmitHelpModal";

export default {
    name: 'ContactPage.vue',
    components: {
        BannerAlert,
        SubmitHelpModal
    },
}
</script>