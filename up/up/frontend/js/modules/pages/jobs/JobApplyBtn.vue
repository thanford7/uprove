<template>
    <a class="btn btn-primary" :href="applicationUrl" target="_blank"
       title="This will take you to the company's job application page">
        Apply <i class="fas fa-external-link-alt -color-white-text"></i>
    </a>
</template>

<script>
export default {
    name: "JobApplyBtn",
    props: ['applicationUrl']
}
</script>