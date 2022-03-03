<template>
    <InputSelectize
        ref="skillLevels"
        :elId="getNewElUid()"
        :isParseAsBits="true"
        :placeholder="(placeholder) ? placeholder : 'Experience Levels: All'"
        :cfg="skillLevelsCfg"
        :items="items"
    />
</template>

<script>
import InputSelectize from "./InputSelectize";
import skillLevelSelectize from "../selectizeCfgs/skillLevels";

export default {
    name: "SkillLevelsSelectize",
    props: ['cfg', 'placeholder', 'items'],
    components: {InputSelectize},
    data() {
        return {
            targetEl: null,
            elSel: null
        }
    },
    computed: {
        skillLevelsCfg() {
            return skillLevelSelectize.getSkillLevelCfg(this.globalData.SKILL_LEVEL, this.cfg);
        }
    },
    mounted() {
        this.targetEl = this.$refs.skillLevels.targetEl;
        this.elSel = this.$refs.skillLevels.elSel;
    }
}
</script>