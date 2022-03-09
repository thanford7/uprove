<template>
    <BasePage headerTitle="Account settings">
        <div class="row">
            <div class="col-md-2 col-12 profile-picture">
                <span id="profilePic">
                    <img src="" alt="Profile picture">
                    <i class="fas fa-pencil-alt" id="editProfile"></i>
                </span>
                <h4 class="-text-center">{{initData.firstName}} {{initData.lastName}}</h4>
            </div>
        </div>
    </BasePage>
</template>

<script>
import BasePage from "../BasePage";

export default {
    name: "AccountSettingsPage.vue",
    components: {BasePage}
}
</script>