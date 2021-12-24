<template>
    <BannerAlert/>
    <div class="row mb-3 ms-0 me-0">
        <div class="col-12 -color-yellow text-center p-2">Are you a talented candidate looking for a job?
            <a href="#" @click="eventBus.emit('open:candidateRequestAccountModal')">Request an account now!</a>
        </div>
        <div class="col-md-6 -color-teal position pt-3 -bg-clip-border">
            <div class="position__center-vertical p-md-5 p-2">
                <h1 class="text-center"><strong>Skills based project exercises and video presentations to assess candidates' true talent</strong></h1>
                <div id="hero-benefits-rotation" class="text-center"></div>
                <div class="text-center mt-4">
                    <button type="button" class="btn btn-lg btn-primary -color-darkblue" @click="eventBus.emit('open:employerRequestInfoModal')">
                        Request demo
                    </button>
                </div>
            </div>
        </div>
        <div class="col-md-6 -color-black -bg-clip-border ps-0 pe-0 d-flex align-items-center">
            <video class="background-video" autoplay loop muted poster="">
              <source :src="globalData.MEDIA_URL + 'ProjectDemo_Hero.mp4'" type="video/mp4">
            </video>
        </div>
    </div>
</template>

<script>
import BannerAlert from "../../components/BannerAlert";

export default {
    name: "HeroBanner.vue",
    components: {BannerAlert}
}
</script>