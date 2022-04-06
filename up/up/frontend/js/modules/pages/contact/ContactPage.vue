<template>
    <BasePage headerTitle="Contact us">
        <div class="row mb-3">
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