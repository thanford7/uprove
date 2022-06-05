<template>
    <div class="col-md-3">
        <div class="card-custom card-custom--no-side-margin card-custom--no-top-margin" :class="(isMobile) ? '' : 'sticky-top'">
            <div class="profile-picture">
                <span id="profilePic">
                    <img v-if="profilePicture" :src="profilePicture.image">
                    <i v-else class="fas fa-user fa-4x"></i>
                    <i
                        v-if="isOwner"
                        class="fas fa-pencil-alt fa-lg"
                        id="editProfile"
                        @click="eventBus.emit('open:editProfileModal', {user, profilePicture, id: profileId})"
                    />
                </span>
                <h6 class="-text-center mt-2">{{user.firstName}} {{user.lastName}}</h6>
                <div v-if="location" class="-text-medium" :title="location">
                    <div class="row">
                        <div class="col-1">
                            <i class="fas fa-map-marker-alt"></i>
                        </div>
                        <div class="col-10">
                            {{location}}
                        </div>
                    </div>
                </div>
            </div>
            <div v-if="user.skills?.length" class="mt-2">
                <div class="-sub-text">SKILLS</div>
                <template v-for="skill in user.skills">
                    <InfoToolTip
                        v-if="skill.description"
                        :elId="getNewElUid()"
                        :content="skill.description"
                        :isExcludeInfoCircle="true"
                        style="display: inline-block;"
                        class="me-1"
                    >
                        <span class="-sub-text badge rounded-pill -color-darkblue -color-white-text">{{skill.title}}</span>
                    </InfoToolTip>
                    <div v-else class="-sub-text badge rounded-pill -color-darkblue -color-white-text me-1" style="display: inline-block;">
                        {{skill.title}}
                    </div>
                </template>
            </div>
            <div v-if="user.interests?.length" class="mt-2">
                <div class="-sub-text">INTERESTS</div>
                <div>
                    <template v-for="interest in user.interests">
                        <InfoToolTip
                            v-if="interest.description"
                            :elId="getNewElUid()"
                            :content="interest.description"
                            :isExcludeInfoCircle="true"
                            style="display: inline-block;"
                            class="me-1"
                        >
                            <span class="-sub-text badge rounded-pill -color-orange -color-white-text">{{interest.title}}</span>
                        </InfoToolTip>
                        <div v-else class="-sub-text badge rounded-pill -color-orange -color-white-text me-1" style="display: inline-block;">
                            {{interest.title}}
                        </div>
                    </template>
                </div>
            </div>
            <div v-if="applicationsHtml">
                <i class="fas fa-lightbulb -color-orange-text"></i>&nbsp;Candidate has
                <InfoToolTip
                    :elId="getNewElUid()"
                    :content="applicationsHtml"
                    :isExcludeInfoCircle="true"
                    :isHtmlContent="true"
                >
                    <u>{{pluralize('application', applications.length)}}</u>
                </InfoToolTip>
                for {{applications[0].employer}}
            </div>
            <a v-if="user.resume && (isEmployer || isOwner)" class="btn btn-outline-info mt-3 w-100" download :href="user.resume">
                <i class="fas fa-file-download"></i> Download resume
            </a>
            <div v-if="isEmployer && !isOwner" class="btn btn-outline-info mt-2 w-100" @click="eventBus.emit('open:saveCandidateModal', user)">
                Invite to interview
            </div>
        </div>
        <SaveCandidateModal
            v-if="isEmployer"
            :employerId="globalData.uproveUser.employerId"
            :applications="applications"
        />
    </div>
</template>

<script>
import InfoToolTip from "../../components/InfoToolTip";
import ProgressPill from "../../components/ProgressPill";
import SaveCandidateModal from "../../modals/SaveCandidateModal";

export default {
    name: "CandidateSideBar",
    props: ['user', 'profilePicture', 'isOwner', 'profileId', 'applications'],
    components: {InfoToolTip, ProgressPill, SaveCandidateModal},
    computed: {
        location() {
            const locationParts = ['city', 'state', 'country'].reduce((locationParts, loc) => {
                if (this.user[loc]) {
                    locationParts.push(this.user[loc]);
                }
                return locationParts;
            }, []);
            if (!locationParts.length) {
                return null;
            }
            return locationParts.join(', ');
        },
        applicationsHtml() {
            if (!this.applications || !this.applications.length) {
                return null;
            }
            let applicationHtml = '<ul>';
            this.applications.forEach((app) => {
                applicationHtml += `<li>${app.jobTitle}</li>`
            })
            applicationHtml += '</ul>';
            return applicationHtml;
        }
    },
}
</script>