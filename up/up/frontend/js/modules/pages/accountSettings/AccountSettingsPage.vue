<template>
    <div class="container-lg">
        <BannerAlert/>
        <div class="row mt-4">
            <div class="col-md-2 col-12 profile-picture">
                <span id="profilePic">
                    <img src="" alt="Profile picture">
                    <i class="fas fa-pencil-alt" id="editProfile"></i>
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