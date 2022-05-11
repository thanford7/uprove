<template>
    <InfoToolTip
        :elId="getNewElUid()"
        :isExcludeInfoCircle="true"
        content="This company is a Uprove partner and actively reviews project submissions"
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