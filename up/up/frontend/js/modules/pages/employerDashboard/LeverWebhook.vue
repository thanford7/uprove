<template>
    <div class="row mt-2 mb-4">
        <p class="-border-bottom--light">
            {{hookName}} <InfoToolTip :elId="getNewElUid()" :content="hookInfo"/>
        </p>
        <div class="col-md-6">
            <span class="-text-medium">Signature Token</span>
            <input
                type="text"
                class="form-control"
                placeholder="Required"
                v-model="leverData[modelName]"
            >
        </div>
        <div class="col-md-6">
            <span class="-text-medium">Webhook URL <i class="fas fa-copy" @click="copyText"></i></span>
            <input
                type="text"
                class="form-control copy-target"
                placeholder="Required"
                disabled
                :value="getLeverWebhookUrl(hookType, employer.id)"
            >
        </div>
    </div>
</template>

<script>
import InfoToolTip from "../../components/InfoToolTip";
import dataUtil from "../../../utils/data";
import leverIntegration from "../../../utils/leverIntegration";

export default {
    name: "LeverWebhook",
    props: ['hookInfo', 'hookName', 'hookType', 'modelName', 'leverData', 'employer'],
    components: {InfoToolTip},
    methods: {
        copyText: dataUtil.copyText,
        getLeverWebhookUrl: leverIntegration.getWebhookUrl.bind(leverIntegration),
    }
}
</script>