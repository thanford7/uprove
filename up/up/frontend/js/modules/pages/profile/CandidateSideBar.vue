<template>
    <div class="col-md-3 col-lg-2 card-custom">
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
            <h4 class="-text-center mt-2">{{user.firstName}} {{user.lastName}}</h4>
        </div>
        <div class="mt-3">
            <span class="-sub-text">SKILLS</span>
            <div v-for="skill in user.skills">
                <span class="-sub-text">{{skill.title}}&nbsp;</span>
                <InfoToolTip v-if="skill.description" :elId="getNewElUid()" :content="skill.description"/>
                <ProgressPill
                    color="darkblue"
                    :pctComplete="getSkillPct(skill)"
                    :text="getSkillText(skill)"
                    :hoverText="getSkillDescription(skill)"
                />
            </div>
        </div>
        <div class="mt-3">
            <span class="-sub-text">INTERESTS</span>
            <div>
                <template v-for="interest in user.interests">
                    <span class="-sub-text">{{interest.title}}&nbsp;</span>
                    <InfoToolTip v-if="interest.description" :elId="getNewElUid()" :content="interest.description"/>&nbsp;
                </template>
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
    methods: {
        getSkillPct(skill) {
            return this.globalData.SKILL_LEVEL[skill.skillLevelBit]?.pct;
        },
        getSkillText(skill) {
            return this.globalData.SKILL_LEVEL[skill.skillLevelBit]?.title;
        },
        getSkillDescription(skill) {
            return this.globalData.SKILL_LEVEL[skill.skillLevelBit]?.description;
        },
    }
}
</script>