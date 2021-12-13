<template>
    <div v-if="alerts.length" v-for="alert in alerts" class="mt-3">
        <div class="alert alert-dismissible fade show" :class="`alert-${alert.alertType}`" role="alert">
            {{alert.message}}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    </div>
</template>

<script>
import {severity} from "../../vueMixins";

export default {
    name: "BannerAlert.vue",
    props: ['alerts'],
    updated() {
        // Close success alerts after 5 seconds
        setTimeout(() => {
            $(`.alert-${severity.SUCCESS}`).alert('close')
        }, 5000);
    }
}
</script>