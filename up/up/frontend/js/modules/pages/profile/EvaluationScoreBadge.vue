<template>
    <InfoToolTip
        :elId="getNewElUid()"
        :content="getEvalPopoverHtml()"
        :isHtmlContent="true"
        :isExcludeInfoCircle="true"
        class="me-1"
    >
        <span v-if="evalScorePct"
              class="badge"
              :class="`
                bg-${getBadgeColor({score: evalScorePct})}
                -color-${getBadgeTextColor({score: evalScorePct})}-text
              `"
              style="mix-blend-mode: darken;"
        >
            Evaluation score: {{evalScorePct}}%
        </span>
    </InfoToolTip>
</template>

<script>
import InfoToolTip from "../../components/InfoToolTip";
import userProjectUtil from "../../../utils/userProject";

export default {
    name: "EvaluationScoreBadge",
    props: ['evalScorePct'],
    components: {InfoToolTip},
    methods: {
        getBadgeColor: userProjectUtil.getBadgeColor,
        getBadgeTextColor: userProjectUtil.getBadgeTextColor,
        getEvalPopoverHtml: userProjectUtil.getEvalPopoverHtml,
    }
}
</script>