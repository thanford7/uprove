<template>
    <header class="site-header">
        <nav class="navbar navbar-expand-md navbar-light -color-lightgrey">
            <div class="container-fluid d-flex">
                <div class="navbar-brand flex-grow-1 -color-orange-text">Uprove</div>
                <font-awesome-icon class="mobile-only" :icon="['fas', 'user-circle']" size="lg"/>
                <div class="navbar-collapse collapse justify-content-end" id="uprove-navbar">
                    <ul class="navbar-nav nav justify-content-end">
                        <template v-if="!userId">
                            <li class="nav-item">
                                <a class="nav-link" href="#">Projects</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="#">Pricing</a>
                            </li>
                        </template>
                        <li class="nav-item desktop-only">
                            <a v-if="!userId" class="nav-link" href="#"><font-awesome-icon :icon="['fas', 'user-circle']"/> Sign in</a>
                            <a v-else class="nav-link" href="#"><font-awesome-icon :icon="['fas', 'user-circle']" size="lg"/></a>
                        </li>
                    </ul>
                </div>
                <button class="navbar-toggler ms-2 mb-1 mt-1" type="button" data-bs-toggle="collapse" data-bs-target="#uprove-navbar">
                    <div class="hamburger">
                        <span class="bar"></span>
                        <span class="bar"></span>
                        <span class="bar"></span>
                    </div>
                </button>
            </div>
        </nav>
    </header>
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