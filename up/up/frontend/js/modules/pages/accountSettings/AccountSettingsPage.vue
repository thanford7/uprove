<template>
    <div class="container-lg">
        <BannerAlert :alerts="alerts"/>
        <div class="row mt-4">
            <div class="col-md-2 col-12 profile-picture">
                <span id="profilePic">
                    <img src="" alt="Profile picture">
                    <font-awesome-icon
                        id="editProfile"
                        :icon="['fas', 'pencil-alt']"
                    />
                </span>
                <h4 class="-text-center">{{initData.firstName}} {{initData.lastName}}</h4>
            </div>
        </div>
    </div>
</template>

<script>
import BannerAlert from "../../components/BannerAlert";
export default {
    name: "AccountSettingsPage.vue",
    components: {BannerAlert}
}
</script>