<template>
    <div class="container-fluid">
        <a class="navbar-brand" href="/">
            <img class="logo" :src="globalData.STATIC_URL + 'img/logo.png'" alt="Uprove">
        </a>
        <div class="navbar-collapse collapse justify-content-end" id="uprove-navbar">
            <ul class="navbar-nav nav justify-content-end">
                <template v-if="!globalData.uproveUser">
                    <li class="nav-item">
                        <a class="nav-link" href="/projects">Projects</a>
                    </li>
                </template>
                <li v-if="!isMobile" class="nav-item" :class="(isMobile) ? '' : 'dropdown'">
                    <a v-if="!globalData.uproveUser" class="nav-link" href="#"
                       @click="eventBus.emit('open:signInModal')">
                        <font-awesome-icon :icon="['fas', 'user-circle']"/>
                        Sign in</a>
                    <a v-else class="nav-link dropdown-toggle no-caret" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false">
                        <font-awesome-icon :icon="['fas', 'user-circle']" size="lg"/>
                    </a>
                    <div class="dropdown-menu dropdown-menu-end">
                        <a class="dropdown-item" href="/account-settings">Account settings</a>
                        <a class="dropdown-item" href="#" @click="submitAjaxRequest({}, {method: 'POST', url: globalData.API_URL + 'logout/'})">Log out</a>
                    </div>
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
            <div class="dropdown show" style="display: inline-block" v-if="isMobile">
              <a class="dropdown-toggle no-caret" href="#" role="button" id="accountDropdownMenu" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <font-awesome-icon class="ms-1 mb-2" :icon="['fas', 'user-circle']" size="lg"/>
              </a>

              <div class="dropdown-menu dropdown-menu-end" aria-labelledby="accountDropdownMenu">
                <a v-if="!globalData.uproveUser" class="dropdown-item" href="#" @click="eventBus.emit('open:signInModal')">Sign in</a>
                  <template v-else>
                        <a class="dropdown-item" href="/account-settings">Account settings</a>
                        <a class="dropdown-item" href="#" @click="submitAjaxRequest({}, {method: 'POST', url: globalData.API_URL + 'logout/'})">Log out</a>
                  </template>
              </div>
            </div>
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
            headerMenu$: null,
            dropdowns: null
        }
    },
    components: {SignInModal},
    methods: {
        hookEvents() {
            // Open dropdown menu when clicked
            this.dropdowns = $('.dropdown-toggle').dropdown();
            this.dropdowns.on('click', (e) => {
                e.preventDefault();
                $(e.currentTarget).dropdown('toggle');
            });

            // Close dropdown menu when clicked outside menu
            $(':not(.dropdown):not(.dropdown-toggle)').on('click', (e) => {
                if ($('.dropdown-menu.show').length > 0 && !$(e.target).parents('.dropdown').length) {
                    $('.dropdown-toggle').dropdown('toggle')
                }
            });
        }
    },
    mounted() {
        this.hookEvents();
    },
    updated() {
        this.hookEvents();
    }
}
</script>