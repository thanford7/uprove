<template>
    <div class="container-fluid" id="header-container">
        <a class="navbar-brand" :href="getHomepageUrl()">
            <img class="logo" :src="globalData.STATIC_URL + 'img/logo.png'" alt="Uprove">
        </a>
        <div class="navbar-collapse collapse justify-content-end" id="uprove-navbar">
            <ul class="navbar-nav nav justify-content-end">
                <li v-if="isSuperUser || isCandidate" :class="(isCurrentUrl('candidateDashboard')) ? 'current-page' : ''">
                    <a class="nav-link" href="/candidateDashboard">Home</a>
                </li>
                <li v-if="isSuperUser || isEmployer" :class="(isCurrentUrl('employerDashboard')) ? 'current-page' : ''">
                    <a class="nav-link" href="/employerDashboard">Employer Dashboard</a>
                </li>
                <li class="nav-item" :class="(isCurrentUrl('projects')) ? 'current-page' : ''">
                    <a class="nav-link" href="/projects">Projects</a>
                </li>
                <li v-if="isSuperUser" class="nav-item" :class="(isCurrentUrl('admin')) ? 'current-page' : ''">
                    <a class="nav-link" href="/admin">Admin</a>
                </li>
                <li v-if="!isMobile" class="nav-item" :class="(isMobile) ? '' : 'dropdown'">
                    <a v-if="!isLoggedIn" class="nav-link" href="#"
                       @click="eventBus.emit('open:signInModal')">
                        <i class="fas fa-user-circle"></i>
                        Sign in</a>
                    <template v-else>
                        <a class="nav-link dropdown-toggle no-caret" data-toggle="dropdown" href="#"
                           role="button" aria-haspopup="true" aria-expanded="false">
                            <i class="fas fa-user-circle fa-lg"></i>
                        </a>
                        <div class="dropdown-menu dropdown-menu-end">
                            <a class="dropdown-item" :href="`/account-settings/${globalData.uproveUser.id}/`">Account
                                settings</a>
                            <a class="dropdown-item" href="#"
                               @click="submitAjaxRequest(null, {method: 'POST', url: globalData.API_URL + 'logout/'})">Log
                                out</a>
                        </div>
                    </template>
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
                <a class="dropdown-toggle no-caret" href="#" role="button" id="accountDropdownMenu"
                   data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    <i class="fas fa-user-circle fa-lg ms-1 mb-2"></i>
                </a>

                <div class="dropdown-menu dropdown-menu-end" aria-labelledby="accountDropdownMenu">
                    <a v-if="!isLoggedIn" class="dropdown-item" href="#"
                       @click="eventBus.emit('open:signInModal')">Sign in</a>
                    <template v-else>
                        <a class="dropdown-item" :href="`/account-settings/${globalData.uproveUser.id}/`">Account
                            settings</a>
                        <a class="dropdown-item" href="#"
                           @click="submitAjaxRequest({}, {method: 'POST', url: globalData.API_URL + 'logout/'})">Log
                            out</a>
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
        getHomepageUrl() {
            if (this.isCandidate) {
                return '/candidateDashboard/';
            }
            if (this.isEmployer) {
                return '/employerDashboard/';
            }
            return '/';
        },
        isCurrentUrl(url) {
            if (!window.location) {
                return false;
            }
            return window.location.pathname.toLowerCase().includes(url.toLowerCase())
        }
    },
    mounted() {
        // Open dropdown menu when clicked
        $('#header-container').on('click', '.dropdown-toggle', (e) => {
            e.preventDefault();
            $(e.currentTarget).dropdown('toggle');
        });

        // Close dropdown menu when clicked outside menu
        $('body').on('click', ':not(.dropdown):not(.dropdown-toggle)', (e) => {
            if ($('.dropdown-menu.show').length > 0 && !$(e.target).parents('.dropdown').length) {
                $('.dropdown-toggle').dropdown('toggle')
            }
        });
    }
}
</script>