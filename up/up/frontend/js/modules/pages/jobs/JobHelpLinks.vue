<template>
    <ul class="fa-ul">
        <li v-if="job.projectIds.length">
            <span class="fa-li">
                <i class="fas fa-external-link-alt"></i>
            </span>
            <a
                :href="getUrlWithParams([{key: 'role', val: [job.roleId]}], '/projects/', true)"
                target="_blank"
            >
                See {{pluralize('Uprove project', job.projectIds.length)}} that
                {{(job.projectIds.length === 1) ? 'showcases' : 'showcase'}} the desired skills for this role
            </a>
        </li>
        <li v-if="employer.glassDoorUrl">
            <span class="fa-li">
                <i class="fas fa-external-link-alt"></i>
            </span>
            <a
                :href="employer.glassDoorUrl"
                target="_blank"
            >
                See Glassdoor info
            </a>
        </li>
    </ul>
</template>

<script>
import dataUtil from "../../../utils/data";

export default {
    name: "JobHelpLinks",
    props: ['job', 'employer'],
    methods: {
        getUrlWithParams: dataUtil.getUrlWithParams.bind(dataUtil),
    }
}
</script>