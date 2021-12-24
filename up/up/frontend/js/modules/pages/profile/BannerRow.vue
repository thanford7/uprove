<template>
    <div class="row -border-bottom--light mb-2 pb-2 ">
        <div class="col-md-2 col-12 profile-picture">
            <span id="profilePic">
                <img :src="profilePicture" alt="Profile picture">
                <i
                    v-if="isOwner"
                    class="fas fa-pencil-alt"
                    id="editProfile"
                    @click="eventBus.$emit('open:editProfileModal')"
                    :data-content-item="profile"
                />
            </span>
            <h4 class="-text-center">{{profile.profile_name}}</h4>
        </div>
        <div class="col-md-10 col-12">
            <h4 class="d-inline-block">Highlights</h4>
            <div v-if="isOwner" class="d-inline-block -no-horizontal-padding">
                <button type="button" class="btn btn-sm btn-outline-secondary" @click="eventBus.$emit('open:addContentModal', 'highlight')">
                    <i class="fas fa-plus"></i> Add card
                </button>
            </div>

            <div class="row grid" id="banner-row">
                <ContentCard
                    v-for="(highlightId, idx) in highlightIds"
                    :key="highlightId"
                    :contentId="highlightId"
                    contentSection="highlight"
                    :contentItemOrder="idx"
                    :isFirstItem="idx === 0"
                    :isLastItem="idx === highlightIds.length - 1"
                />
            </div>
        </div>
    </div>
</template>
<script>
import {mapState} from 'vuex';
import ContentCard from './ContentCard.vue';
import dataUtil from '../../../utils/data';

export default {
    computed: mapState({
        highlightIds: 'highlightIds',
        profilePicture: 'profilePicture',
        profile: 'profile',
        isOwner: 'isOwner',
        eventBus: 'eventBus',
        crudUrl: 'crudUrlProfile'
    }),
    components: {ContentCard},
    methods: {
        onSaveSuccess(requestData, responseData) {
            this.$store.commit(`setHighlightIds`, dataUtil.parseIdString(requestData.highlight_ids));
        }
    },
    mounted() {
        // Position edit profile icon 40% below the start of the profile picture
        $('#editProfile').css('top', `${$('#profilePic img').height() / (10 / 4)}px`);
    }
}
</script>