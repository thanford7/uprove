<template>
    <div class="container-fluid">
        <a class="navbar-brand" href="/">
            <img class="logo" src="/static/img/logo.png" alt="Uprove">
        </a>
        <div class="navbar-collapse collapse justify-content-end" id="uprove-navbar">
            <ul class="navbar-nav nav justify-content-end">
                <template v-if="!userId">
                    <li class="nav-item">
                        <a class="nav-link" href="/projects">Projects</a>
                    </li>
                </template>
                <li v-if="!isMobile" class="nav-item">
                    <a v-if="!userId" class="nav-link" href="#" @click="eventBus.emit('open:signInModal')">
                        <font-awesome-icon :icon="['fas', 'user-circle']"/>
                        Sign in</a>
                    <a v-else class="nav-link" href="/account-settings">
                        <font-awesome-icon :icon="['fas', 'user-circle']" size="lg"/>
                    </a>
                </li>
            </ul>
        </div>
        <div class="justify-content-end align-items-center" style="margin-left: auto;">
            <button class="navbar-toggler ms-2 mb-1 mt-1" type="button" data-bs-toggle="collapse"
                    data-bs-target="#uprove-navbar">
                <div class="hamburger">
                    <span class="bar"></span>
                    <span class="bar"></span>
                    <span class="bar"></span>
                </div>
            </button>
            <font-awesome-icon class="ms-1 mb-2" v-if="isMobile" :icon="['fas', 'user-circle']" size="lg"/>
        </div>
    </div>
    <SignInModal/>
</template>
<script>
import SignInModal from "../../modals/SignInModal";

export default {
    data() {
        return {
            hamburger$: null,
            headerMenu$: null
        }
    },
    components: {SignInModal},
    props: {
        userId: {
            type: Number
        },
        postType: {
            type: String
        }
    }
}
</script>