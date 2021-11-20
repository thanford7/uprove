<template>
    <div>
        <div class="row mt-3 mb-3">
            <h1>Projects</h1>
            <h3>Coming soon...</h3>
            <button v-if="globalData.uproveUser && globalData.uproveUser.isSuperUser" type="button" class="btn btn-secondary" @click="submitAjaxRequest({}, {method: 'GET', url: '/api/v1/user-storage/'})">Upload</button>
        </div>
    </div>
</template>

<script>
export default {
    name: "ProjectsPage.vue"
}
</script>

<style scoped>

</style>