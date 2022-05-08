<template>
    <InfoToolTip
        :elId="getNewElUid()"
        :isExcludeInfoCircle="true"
        content="Uprove talent experts work directly with this company to promote candidates who complete a Uprove project"
    >
        <i class="fas fa-star -color-orange-text"></i>
    </InfoToolTip>
</template>

<script>
import InfoToolTip from "../../components/InfoToolTip";

export default {
    name: "UprovePartner",
    components: {InfoToolTip}
}
</script>