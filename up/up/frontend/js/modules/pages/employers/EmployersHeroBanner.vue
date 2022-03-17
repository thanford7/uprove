<template>
    <div id="employer-hero-banner" class="-z-40">
        <div class="container-lg">
            <div class="content row align-items-center">
                <div class="col-md-7 ps-md-5">
                    <div class="p-4">
                        <h1 id="header-main">
                            <span id="header-line-1">Don't miss out on</span>
                            <span id="header-line-2" class="-color-orange-text" style="letter-spacing: 0.5rem;">hidden talent</span>
                        </h1>
                        <h5 class="mt-4">
                            We uncover <span class="-color-orange-text fw-bold">undiscovered talent</span> by allowing career
                            starters and career switchers to <span class="-color-orange-text fw-bold">prove their skills</span>
                            through real world business projects similar to the work you need them to do
                        </h5>
                        <div class="mt-4">
                            <button type="button" class="btn btn-lg btn-primary button-interactive" @click="signUpWithContext">
                                Talk to a talent expert
                            </button>
                        </div>
                    </div>
                </div>
                <div class="col-md-5 pe-md-4 pb-3 employer-search">
                    <img class="hidden" :src="globalData.STATIC_URL + 'img/icons/ghost.png'"> <!-- Needed to set the height of the container -->
                    <img class="primary" :src="globalData.STATIC_URL + 'img/icons/ghost.png'">
                    <img class="worker-1" :src="globalData.STATIC_URL + 'img/icons/employee-f2.png'">
                    <img class="worker-2" :src="globalData.STATIC_URL + 'img/icons/employee-f.png'">
                    <img class="worker-3" :src="globalData.STATIC_URL + 'img/icons/employee-m3.png'">
                    <img class="worker-4" :src="globalData.STATIC_URL + 'img/icons/employee-f3.png'">
                    <img class="worker-5" :src="globalData.STATIC_URL + 'img/icons/employee-m.png'">
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "EmployersHeroBanner",
    mounted() {
        const ghostDisappearSeconds = 10;
        [1, 2, 3, 4, 5].forEach((workerIdx) => {
            setTimeout(() => {
                $(`.worker-${workerIdx}`).remove();
            }, workerIdx * ghostDisappearSeconds * 1000);
        });
    }
}
</script>