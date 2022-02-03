<template>
    <div v-if="alerts.length" v-for="alert in alerts" class="mt-3 banner-alert">
        <div class="alert alert-dismissible fade show" :class="`alert-${alert.alertType}`" role="alert">
            {{alert.message}}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close" @click="clearAlert(alert.id)"></button>
        </div>
    </div>
</template>

<script>
import {mapMutations, mapState} from "vuex";

export default {
    name: "BannerAlert.vue",
    computed: mapState(['alerts']),
    methods: {
        ...mapMutations(['clearAlert'])
    },
}
</script>