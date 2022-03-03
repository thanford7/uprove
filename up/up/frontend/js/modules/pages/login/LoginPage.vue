<template>
    <BasePage headerTitle="Login">
        <div class="row mt-3 mb-3">
            <div class="col-md-4">
                <form>
                    <div class="mb-3">
                        <label for="loginEmail" class="form-label">Email</label>
                        <InputEmail elId="loginEmail" placeholder="myemail@gmail.com" v-model="formData.email"/>
                    </div>
                    <div class="mb-3">
                        <label for="loginPassword" class="form-label">Password</label>
                        <input type="password" class="form-control" id="loginPassword" placeholder="Required" v-model="formData.password">
                    </div>
                    <button type="submit" class="btn btn-primary" @click="saveChange">Login</button>
                </form>
            </div>
        </div>
    </BasePage>
</template>

<script>
import dataUtil from "../../../utils/data";
import InputEmail from "../../inputs/InputEmail";
import BasePage from "../BasePage";

export default {
    name: "LoginPage.vue",
    components: {BasePage, InputEmail},
    data() {
        return {
            crudUrl: 'login/',
            requiredFields: {
                email: 'loginEmail',
                password: 'loginPassword'
            }
        }
    },
    methods: {
        getAjaxCfgOverride() {
            return {method: 'POST'}
        },
        processFormData() {
            // Add redirect to next page if exists
            return Object.assign(this.readForm(), {next: dataUtil.getQueryParams().next})
        }
    }
}
</script>