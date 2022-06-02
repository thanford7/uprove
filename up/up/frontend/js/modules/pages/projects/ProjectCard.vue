<template>
    <BaseCard :cardItem="this.cardItem" :elId="getNewElUid()" :isShowViewMoreLink="false">
        <template v-slot:topImage>
            <img
                :src="(cardItem.image) ? cardItem.image : (globalData.STATIC_URL + 'img/logo.png')"
                class="card-img-top"
                loading="lazy"
            >
        </template>
        <template v-slot:header>
            {{cardItem.title}}
        </template>
        <template v-slot:body>
            <ProjectJobs :jobs="cardItem.jobs" class="mb-2"/>
            <div class="mb-1 pb-1 -border-bottom--light">
                <div class="text-label text-label-sm">CAREER LEVEL</div>
                <BadgesSkillLevels :skillLevels="cardItem.skillLevels"/>
            </div>
            <div class="mb-1 pb-1 -border-bottom--light">
                <div class="text-label text-label-sm">SKILLS</div>
                <BadgesSkills :skills="cardItem.skills"/>
            </div>
            <div v-html="cardItem.description"></div>
            <ViewMoreLink :href="`/project/${cardItem.id}/`" text="View project details" :elId="getNewElUid()"/>
        </template>
    </BaseCard>
</template>

<script>
import BadgesSkillLevels from "../../components/BadgesSkillLevels";
import BadgesSkills from "../../components/BadgesSkills";
import BaseCard from "../../components/BaseCard";
import ProjectJobs from "./ProjectJobs";
import ViewMoreLink from "../../components/ViewMoreLink";

export default {
    name: "cardItemCard.vue",
    extends: BaseCard,
    inheritAttrs: false,
    components: {BadgesSkillLevels, BadgesSkills, BaseCard, ProjectJobs, ViewMoreLink},
}
</script>