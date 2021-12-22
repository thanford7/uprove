<template>
    <template v-for="(skill, idx) in skills">
        <div class="badge -color-lightblue -color-black-text" :class="(idx !== skills.length - 1) ? 'me-1' : ''">{{skill.skillName}}</div>
    </template>
</template>

<script>
export default {
    name: "BadgesSkills.vue",
    props: ['skills']
}
</script>