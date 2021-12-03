<template>
    <BaseCard :cardItem="this.cardItem" :elId="newElUid" :isShowViewMoreLink="false">
        <template v-slot:topImage>
            <img :src="(cardItem.image) ? cardItem.image : (globalData.STATIC_URL + 'img/logo.png')" class="card-img-top">
        </template>
        <template v-slot:header>
            {{cardItem.title}}<span class="badge -color-darkblue float-end">{{cardItem.function}}</span>
        </template>
        <template v-slot:body>
            <div class="mb-1 pb-1 -border-bottom--light">
                <div class="text-label text-label-sm">CAREER LEVELS</div>
                <BadgesSkillLevels :skillLevels="cardItem.skillLevels"/>
            </div>
            <div class="mb-1 pb-1 -border-bottom--light">
                <div class="text-label text-label-sm">SKILLS</div>
                <BadgesSkills :skills="cardItem.skills"/>
            </div>
            <div v-html="cardItem.description"></div>
            <ViewMoreLink :href="`/project/${cardItem.id}/`" text="View project details" :elId="newElUid"/>
        </template>
    </BaseCard>
</template>

<script>
import BadgesSkillLevels from "./BadgesSkillLevels";
import BadgesSkills from "./BadgesSkills";
import BaseCard from "./BaseCard";
import ViewMoreLink from "./ViewMoreLink";

export default {
    name: "cardItemCard.vue",
    extends: BaseCard,
    inheritAttrs: false,
    components: {BadgesSkillLevels, BadgesSkills, BaseCard, ViewMoreLink}
}
</script>