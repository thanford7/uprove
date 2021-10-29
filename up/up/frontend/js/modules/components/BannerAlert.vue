<template>
    <div v-if="alerts.length" v-for="alert in alerts" class="mt-3">
        <div class="alert alert-dismissible fade show" :class="`alert-${alert.alertType}`" role="alert">
            {{alert.message}}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    </div>
</template>

<script>
export default {
    name: "BannerAlert.vue",
    props: ['alerts']
}
</script>