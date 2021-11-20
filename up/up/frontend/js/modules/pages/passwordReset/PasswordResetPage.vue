<template>
    <BannerAlert :alerts="alerts"/>
    <div>
        <div class="row mt-3 mb-3">
            <h2>Password Reset</h2>
            <div class="col-md-4">
                <form>
                    <div class="mb-3">
                        <label for="passwordReset" class="form-label">Password</label>
                        <input type="password" class="form-control" id="passwordReset" placeholder="Required" v-model="formData.password">
                        <div class="mt-3">
                            Password must have:
                            <ul>
                                <li>8 characters minimum<span v-if="has8Char">&nbsp;<font-awesome-icon :icon="['fas', 'check']" class="-color-green-fa"/></span></li>
                                <li>At least 1 lowercase letter<span v-if="hasLowercaseChar">&nbsp;<font-awesome-icon :icon="['fas', 'check']" class="-color-green-fa"/></span></li>
                                <li>At least 1 uppercase letter<span v-if="hasUppercaseChar">&nbsp;<font-awesome-icon :icon="['fas', 'check']" class="-color-green-fa"/></span></li>
                                <li>At least 1 number<span v-if="hasNumber">&nbsp;<font-awesome-icon :icon="['fas', 'check']" class="-color-green-fa"/></span></li>
                                <li>At least one symbol<span v-if="hasSymbolChar">&nbsp;<font-awesome-icon :icon="['fas', 'check']" class="-color-green-fa"/></span></li>
                            </ul>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="passwordConfirm" class="form-label">Password</label>
                        <input type="password" class="form-control" id="passwordConfirm" placeholder="Required" v-model="formData.passwordConfirm">
                        <div v-if="hasPasswordConfirmMatch" class="mt-3">Passwords match&nbsp;<font-awesome-icon :icon="['fas', 'check']" class="-color-green-fa"/></div>
                    </div>
                    <button type="submit" class="btn btn-primary" @click="saveChange($event, true)">Save password</button>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import BannerAlert from "../../components/BannerAlert";
import $ from "jquery";
export default {
    name: "PasswordResetPage.vue",
    components: {BannerAlert},
    data() {
        return {
            crudUrl: 'setPassword/',
            requiredFields: {
                password: 'passwordReset'
            }
        }
    },
    computed: {
        has8Char() {
            return this.formData.password && this.formData.password.length >= 8;
        },
        hasUppercaseChar() {
            return this.formData.password && this.formData.password.search(/[A-Z]/) >= 0;
        },
        hasLowercaseChar() {
            return this.formData.password && this.formData.password.search(/[a-z]/) >= 0;
        },
        hasNumber() {
            return this.formData.password && this.formData.password.search(/[0-9]/) >= 0;
        },
        hasSymbolChar() {
            return this.formData.password &&
                this.formData.password.search(/[^A-Za-z0-9]/) >=0 &&
                this.formData.password.search(/\s/) === -1;
        },
        hasPasswordConfirmMatch() {
            return this.formData.password && this.formData.passwordConfirm && this.formData.password === this.formData.passwordConfirm;
        }
    },
    methods: {
        getAjaxCfgOverride() {
            return {method: 'POST'}
        },
        isGoodFormFields(formData) {
            if (![this.has8Char, this.hasUppercaseChar, this.hasLowercaseChar, this.hasNumber, this.hasSymbolChar].every(x => x)) {
                this.addPopover($('#passwordReset'), {content: 'Password requirements not met', isOnce: true});
                return false;
            }
            if (!this.hasPasswordConfirmMatch) {
                this.addPopover($('#passwordConfirm'), {content: 'Password confirmation must match', isOnce: true});
                return false;
            }
            return true;
        },
        processFormData() {
            return Object.assign({}, this.readForm(), {uproveUserId: (this.globalData.uproveUser) ? this.globalData.uproveUser.id : null})
        },
        warnUnsuccessfulPasswordReset() {
            if (djangoData.title === 'Password reset unsuccessful') {
                this.alerts.push({
                    message: djangoData.title,
                    alertType: 'danger'
                });
            }
        }
    },
    mounted() {
        this.warnUnsuccessfulPasswordReset();
    },
    updated() {
        this.warnUnsuccessfulPasswordReset();
    }
}
</script>