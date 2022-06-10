<template>
    <div v-if="!isLoading" class="collapse-card card-custom card-custom--no-top-margin">
        <slot name="top"></slot>
        <CollapseDiv :elId="getNewElUid()" class="-border-bottom--light" :isClosed="!isCompanyDescriptionOpen">
            <template v-slot:header>Company Profile</template>
            <div v-html="employer.description"></div>
        </CollapseDiv>
        <CollapseDiv :elId="getNewElUid()" class="-border-bottom--light" :isClosed="!isJobDescriptionOpen">
            <template v-slot:header>Job Description</template>
            <div class="job-description" v-html="job.jobDescription"></div>
        </CollapseDiv>
        <slot name="bottom"></slot>
    </div>
</template>

<script>
import CollapseDiv from "../../components/CollapseDiv";

export default {
    name: "JobPosting",
    components: {CollapseDiv},
    props: ['employer', 'job', 'isJobDescriptionOpen', 'isCompanyDescriptionOpen'],
}
</script>