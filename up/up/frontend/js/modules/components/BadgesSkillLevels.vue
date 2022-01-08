<template>
    <template v-for="(skillLevel, idx) in skillLevels">
        <div class="badge -color-lightgrey -color-black-text me-1">
            {{skillLevel.title}} <InfoToolTip :content="skillLevel.description" :elId="getNewElUid()"/>
        </div>
    </template>
</template>

<script>
import InfoToolTip from "./InfoToolTip";

export default {
    name: "BadgesSkillLevels.vue",
    props: ['skillLevels'],
    components: {InfoToolTip},
    data() {
        return {

        }
    }
}
</script>