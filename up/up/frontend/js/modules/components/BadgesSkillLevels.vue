<template>
    <template v-for="(skillLevel, idx) in skillLevels">
        <div class="badge -color-lightgrey -color-black-text me-1">{{skillLevel}}</div>
    </template>
</template>

<script>
export default {
    name: "BadgesSkillLevels.vue",
    props: ['skillLevels']
}
</script>