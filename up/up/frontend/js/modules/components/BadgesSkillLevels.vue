<template>
    <template v-for="(skillLevel, idx) in skillLevels">
        <div class="badge -color-lightgrey -color-black-text" :class="(idx !== skillLevels.length - 1) ? 'me-1' : ''">{{skillLevel}}</div>
    </template>
</template>

<script>
export default {
    name: "BadgesSkillLevels.vue",
    props: ['skillLevels']
}
</script>