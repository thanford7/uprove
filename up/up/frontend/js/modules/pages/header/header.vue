<template>
    <div class="container-fluid">
        <a class="navbar-brand" href="/">
            <img class="logo" src="/static/img/logo.png" alt="Uprove">
        </a>
        <font-awesome-icon v-if="isMobile" :icon="['fas', 'user-circle']" size="lg"/>
        <div class="navbar-collapse collapse justify-content-end" id="uprove-navbar">
            <ul class="navbar-nav nav justify-content-end">
                <template v-if="!userId">
                    <li class="nav-item">
                        <a class="nav-link" href="#">Projects</a>
                    </li>
                </template>
                <li v-if="!isMobile" class="nav-item">
                    <a v-if="!userId" class="nav-link" href="#">
                        <font-awesome-icon :icon="['fas', 'user-circle']"/>
                        Sign in</a>
                    <a v-else class="nav-link" href="#">
                        <font-awesome-icon :icon="['fas', 'user-circle']" size="lg"/>
                    </a>
                </li>
            </ul>
        </div>
        <button class="navbar-toggler ms-2 mb-1 mt-1" type="button" data-bs-toggle="collapse"
                data-bs-target="#uprove-navbar">
            <div class="hamburger">
                <span class="bar"></span>
                <span class="bar"></span>
                <span class="bar"></span>
            </div>
        </button>
    </div>
</template>
<script>
export default {
    data() {
        return {
            hamburger$: null,
            headerMenu$: null
        }
    },
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