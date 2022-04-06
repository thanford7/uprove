<template>
    <BasePage :headerTitle="`Error: ${initData.error}`">
        <div class="card-custom">
            <h4>{{initData.text}}</h4>
        </div>
    </BasePage>
</template>

<script>
import BasePage from "../base/BasePage";
export default {
    name: "ErrorsPage.vue",
    components: {BasePage}
}
</script>