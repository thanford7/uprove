<template>
    <BasePage headerTitle="Contact us">
        <div class="row mb-3" :class="(isMobile) ? 'mobile-top' : ''">
            <div class="col-md-6 card-custom card-custom--no-side-margin">
                <SubmitHelpModal ref="submitHelp" :isContentOnly="true"/>
                <button type="submit" class="btn btn-primary" @click="$refs['submitHelp'].saveChange($event)">Send message</button>
            </div>
            <div class="col-md-6 ps-6 pe-6">
                <img
                    :src="globalData.STATIC_URL + 'img/icons/phone-call-512.png'"
                    alt="Customer support"
                    :style="(isMobile) ? 'max-height: 25vh' : ''"
                >
            </div>
        </div>
    </BasePage>
</template>

<script>
import BannerAlert from "../../components/BannerAlert";
import SubmitHelpModal from "../../modals/SubmitHelpModal";
import BasePage from "../base/BasePage";

export default {
    name: 'ContactPage.vue',
    components: {
        BasePage,
        BannerAlert,
        SubmitHelpModal
    },
}
</script>