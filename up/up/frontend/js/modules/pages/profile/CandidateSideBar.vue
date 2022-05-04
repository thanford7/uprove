<template>
    <div class="col-md-3 col-lg-2">
        <div class="card-custom card-custom--no-side-margin card-custom--no-top-margin" :class="(isMobile) ? '' : 'sticky-top'">
            <div class="profile-picture">
                <span id="profilePic">
                    <img v-if="profilePicture" :src="profilePicture.image">
                    <i v-else class="fas fa-user fa-4x"></i>
                    <i
                        v-if="isOwner"
                        class="fas fa-pencil-alt fa-lg"
                        id="editProfile"
                        @click="eventBus.emit('open:editProfileModal', initData)"
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
        </div>
    </div>
</template>

<script>
import InfoToolTip from "../../components/InfoToolTip";
import ProgressPill from "../../components/ProgressPill";
export default {
    name: "CandidateSideBar",
    props: ['user', 'profilePicture', 'isOwner'],
    components: {InfoToolTip, ProgressPill},
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
        }
    },
    methods: {
        getSkillPct(skill) {
            return this.globalData.SKILL_LEVEL[skill.skillLevelBit]?.pct;
        },
    }
}
</script>