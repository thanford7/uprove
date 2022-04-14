<template>
    <BasePage :headerTitle="`${initData.employer.companyName}: Uprove Assessment Configuration`" :headerImage="initData.employer.logo">
        <div class="row">
            <div>
                <h5>Assessment for {{initData.candidate.name}}</h5>
            </div>
        </div>
    </BasePage>
</template>

<script>
import BasePage from "../base/BasePage";

export default {
    name: "LeverSendOpportunityPage",
    components: {BasePage}
}
</script>