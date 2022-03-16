<template>
    <div id="candidate-hero-banner" class="-z-60">
        <div class="container-lg">
            <div class="content row align-items-center">
                <div class="col-md-7 ps-md-5">
                    <div class="p-4">
                        <h1 id="header-main">
                            <span id="header-line-1">Real world business projects to</span>
                            <span id="header-line-2" class="-color-orange-text" style="letter-spacing: 0.5rem;">prove your skills</span>
                            <span id="header-line-3">to employers</span>
                        </h1>
                        <h5 class="mt-4">
                            Flip the script. Stop applying to hundreds of jobs without hearing back. Complete
                            a project and let employers come to you!
                        </h5>
                        <div class="mt-4">
                            <button type="button" class="btn btn-lg btn-primary button-interactive" @click="signUpWithContext">
                                Create account
                            </button>
                        </div>
                    </div>
                </div>
                <div class="col-md-5 pe-md-4 pb-3">
                    <img id="project-example" :src="globalData.STATIC_URL + 'img/profileProjectExample.png'">
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import dataUtil from "../../../utils/data";

export default {
    name: "CandidateHeroBanner",
    methods: {
        signUpWithContext() {
            dataUtil.signUpWithContext(this.initData);
        }
    }
}
</script>