<template>
    <div class="row mt-3 mb-5">
        <h5 class="mb-4">Placing job seekers at amazing companies</h5>
        <div class="col-12">
            <div class="row">
                <div class="col-md-3 col-6 mt-3">
                    <img
                        :src="globalData.STATIC_URL + 'img/amazonLogo.png'"
                        alt="Amazon"
                        style="max-height: 30px;"
                    >
                </div>
                <div class="col-md-3 col-6 mt-3">
                    <img
                        :src="globalData.STATIC_URL + 'img/cabinetHealthLogo.png'"
                        alt="Cabinet Health"
                        style="max-height: 30px;"
                    >
                </div>
                <div class="col-md-3 col-6 mt-3">
                    <img
                        :src="globalData.STATIC_URL + 'img/healthmonixLogo.png'"
                        alt="Healthmonix"
                        style="max-height: 30px;"
                    >
                </div>
                <div class="col-md-3 col-6 mt-3">
                    <img
                        :src="globalData.STATIC_URL + 'img/trueFootageLogo.png'"
                        alt="True Footage"
                        style="max-height: 30px;"
                    >
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "CompanyLogos"
}
</script>