<template>
    <div class="container-fluid" id="header-container">
        <a class="navbar-brand" :href="getHomepageUrl()">
            <img class="logo" :src="globalData.STATIC_URL + 'img/logo.png'" alt="Uprove">
        </a>
        <div class="navbar-collapse collapse justify-content-end" id="uprove-navbar">
            <ul class="navbar-nav nav justify-content-end">
                <li v-if="isSuperUser || isCandidate" :class="getHighlightClass('candidateDashboard')">
                    <a class="nav-link nav-link-tight" href="/candidateDashboard">{{(isEmployer) ? 'Candidate Dashboard' : 'Dashboard'}}</a>
                </li>
                <li v-if="globalData.uproveUser && globalData.uproveUser.defaultProfileId" :class="getHighlightClass('profile')">
                    <a class="nav-link nav-link-tight" :href="`/profile/${globalData.uproveUser.defaultProfileId}/`">Profile</a>
                </li>
                <li v-if="isSuperUser || isEmployer" :class="getHighlightClass('employerDashboard')">
                    <a class="nav-link nav-link-tight" href="/employerDashboard">{{(isCandidate) ? 'Employer Dashboard' : 'Dashboard'}}</a>
                </li>
                <li v-if="!isLoggedIn && getIsCurrentUrl('employers')" class="nav-item">
                    <a class="nav-link nav-link-tight" href="/">For Candidates</a>
                </li>
                <li v-if="!isLoggedIn" class="nav-item" :class="getHighlightClass('employers')">
                    <a class="nav-link nav-link-tight" href="/employers">For Employers</a>
                </li>
                <li class="nav-item" :class="getHighlightClass('courses')">
                    <a class="nav-link nav-link-tight" href="/courses">Courses</a>
                </li>
                <li v-if="isSuperUser || isCandidate" class="nav-item" :class="getHighlightClass('jobs')">
                    <a class="nav-link nav-link-tight" href="/jobs">Jobs</a>
                </li>
                <li class="nav-item" :class="getHighlightClass('blog')">
                    <a class="nav-link nav-link-tight" href="/blog">Blog</a>
                </li>
                <li v-if="isSuperUser || isEmployer" class="nav-item" :class="getHighlightClass('candidate-board')">
                    <a class="nav-link nav-link-tight" href="/candidate-board">Candidate Board</a>
                </li>
                <li v-if="isSuperUser" class="nav-item" :class="getHighlightClass('admin')">
                    <a class="nav-link nav-link-tight" href="/admin">Admin</a>
                </li>
                <li v-if="!isMobile" class="nav-item nav-link-tight" :class="(isMobile) ? '' : 'dropdown'">
                    <a v-if="!isLoggedIn" class="nav-link nav-link-tight" href="#"
                       @click="eventBus.emit('open:signInModal')">
                        <i class="fas fa-user-circle"></i>
                        Sign in</a>
                    <template v-else>
                        <a class="nav-link nav-link-tight dropdown-toggle no-caret" data-toggle="dropdown" href="#"
                           role="button" aria-haspopup="true" aria-expanded="false">
                            <i class="fas fa-user-circle fa-lg"></i>
                        </a>
                        <div class="dropdown-menu dropdown-menu-end">
<!--                            <a-->
<!--                                class="dropdown-item"-->
<!--                               :href="`/account-settings/${globalData.uproveUser.id}/`"-->
<!--                            >-->
<!--                                Account settings-->
<!--                            </a>-->
                            <a class="dropdown-item" href="#"
                               @click="submitAjaxRequest(null, {method: 'POST', url: globalData.API_URL + 'logout/'})">Log
                                out</a>
                        </div>
                    </template>
                </li>
                <template v-else>
                    <li v-if="!isLoggedIn" class="nav-item">
                        <a class="nav-link nav-link-tight" href="#" @click="eventBus.emit('open:signInModal')">Sign in</a>
                    </li>
                    <template v-else>
<!--                        <li class="nav-item">-->
<!--                            <a class="nav-link nav-link-tight" :href="`/account-settings/${globalData.uproveUser.id}/`">Account-->
<!--                                settings</a>-->
<!--                        </li>-->
                        <li class="nav-item">
                            <a class="nav-link nav-link-tight" :href="`/account-settings/${globalData.uproveUser.id}/`">Log out</a>
                        </li>
                    </template>
                </template>
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
        </div>
    </div>
    <SignInModal/>
    <ResetPasswordModal/>
</template>
<script>
import dataUtil from "../../../utils/data";
import ResetPasswordModal from "../../modals/ResetPasswordModal";
import SignInModal from "../../modals/SignInModal";

export default {
    data() {
        return {
            hamburger$: null,
            headerMenu$: null,
            dropdowns: null
        }
    },
    components: {ResetPasswordModal, SignInModal},
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
        getIsCurrentUrl(url) {
            return window.location.pathname.toLowerCase().includes(url.toLowerCase());
        },
        getHighlightClass(url) {
            if (!window.location) {
                return '';
            };
            if (this.getIsCurrentUrl(url)) {
                if (this.isMobile) {
                    return '-text-bold';
                }
                return 'current-page -text-bold';
            }
            return '';
        },
        signUpWithContext() {
            dataUtil.signUpWithContext(this.initData);
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