<template>
    <InputSelectize
        ref="skills"
        :elId="getNewElUid()"
        :isParseAsInt="true"
        placeholder="Skills: All"
        :cfg="skillsCfg"
        :items="items"
    />
</template>

<script>
import InputSelectize from "./InputSelectize";
import skillSelectize from "../selectizeCfgs/skill";

export default {
    name: "SkillsSelectize",
    props: ['skills', 'cfg', 'items'],
    data() {
        return {
            targetEl: null,
            elSel: null
        }
    },
    components: {InputSelectize},
    computed: {
        skillsCfg() {
            return skillSelectize.getSkillCfg(this.skills, this.cfg);
        }
    },
    methods: {
        setValue(val) {
            this.$refs.skills.elSel.setValue(val);
        },
        getSkills(skillIds) {
            return (skillIds) ? this.initData.skills.reduce((skills, s) => {
                if (skillIds.includes(s.id)) {
                    skills.push(s.name);
                }
                return skills;
            }, []) : [];
        }
    },
    mounted() {
        this.targetEl = this.$refs.skills.targetEl;
        this.elSel = this.$refs.skills.elSel;
    }
}
</script>