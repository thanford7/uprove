<template>
    <BasePage headerTitle="Contact us">
        <div class="row mb-3">
            <div class="col-md-5 pt-3 call-out-box" :class="(isMobile) ? 'mb-3' : ''">
                <component :is="(isMobile) ? 'h6' : 'h2'">We want you to have a fantastic hiring experience.</component>
                <i class="fas fa-chart-line" :class="(isMobile) ? 'fa-2x' : 'fa-4x'"></i>
                <component :is="(isMobile) ? 'h6' : 'h2'">Connect with one of our project experts to see how we can help.</component>
            </div>
            <div class="col-md-6 card-custom">
                <SubmitHelpModal ref="submitHelp" :isContentOnly="true"/>
                <button type="submit" class="btn btn-primary" @click="$refs['submitHelp'].saveChange($event)">Send message</button>
            </div>
        </div>
    </BasePage>
</template>

<script>
import BannerAlert from "../../components/BannerAlert";
import SubmitHelpModal from "../../modals/SubmitHelpModal";
import BasePage from "../BasePage";

export default {
    name: 'ContactPage.vue',
    components: {
        BasePage,
        BannerAlert,
        SubmitHelpModal
    },
}
</script>