<template>
    <Table :data="allSkills" :headers="headers">
        <template v-slot:body>
            <template v-for="(skill, idx) in allSkills">
                <tr v-if="!skill.isEdit" @click="updateEdit(idx)">
                    <td>{{skill.name}}</td>
                    <td>
                        <BadgesSkillLevels v-if="skill.skillLevelBits" :skillLevels="skill.skillLevels"/>
                        <span v-else>All</span>
                    </td>
                    <td>{{getSkillPriorityLabel(skill)}}</td>
                    <td><i class="fas fa-trash -color-red-text" @click="deleteSkill(idx)" title="Remove skill"></i></td>
                </tr>
                <template v-else>
                    <tr>
                        <td class="border-bottom-0">
                            <InputSelectize
                                v-if="!skill.id"
                                :cfg="getSkillSelectizeCfg()"
                                :elId="getNewElUid()"
                                :items="skill.id"
                                :isParseAsInt="true"
                                @selected="setSkillName(skill, $event)"
                            />
                            <span v-else>{{skill.name}}</span>
                        </td>
                        <td class="border-bottom-0">
                            <InputSelectize
                                :cfg="getSkillLevelsCfg()"
                                :elId="getNewElUid()"
                                :items="getSkillLevelNumbersFromBits(skill.skillLevelBits)"
                                :isParseAsBits="true"
                                @selected="setProjectSkillLevels(skill, $event)"
                            />
                        </td>
                        <td class="border-bottom-0">
                            <InputSelectize
                                :cfg="getSkillPriorityCfg()"
                                :elId="getNewElUid()"
                                :items="getSkillPriorityLabel(skill)"
                                @selected="setSkillPriority(skill, $event)"
                            />
                        </td>
                        <td class="border-bottom-0">
                            <i class="fas fa-check-square -color-green-text" @click="updateEdit(-1)"></i>
                        </td>
                    </tr>
                    <tr>
                        <td colspan="4" class="border-top-0">
                            <textarea
                                rows="3" class="form-control"
                                placeholder="Description"
                                v-model="skill.instruction"
                            />
                        </td>
                    </tr>
                </template>
            </template>
        </template>
        <template v-slot:footer>
            <a href="#" @click="addSkill"><i class="fas fa-plus -color-green-text"></i> Add skill</a>
        </template>
    </Table>
</template>

<script>
import BadgesSkillLevels from "./BadgesSkillLevels";
import dataUtil from "../../utils/data";
import InputSelectize from "../inputs/InputSelectize";
import skillPriority from "../selectizeCfgs/skillPriority";
import skillLevelSelectize from "../selectizeCfgs/skillLevels";
import skillSelectize from "../selectizeCfgs/skill";
import Table from "./Table";
import skillPrioritySelectize from "../selectizeCfgs/skillPriority";

export default {
    name: "EditSkillsTable",
    components: {BadgesSkillLevels, InputSelectize, Table},
    props: ['skills'],
    data() {
        return {
            headers: [[{value: 'Name'}, {value: 'Skill levels'}, {value: 'Priority'}, {}]],
            allSkills: []
        }
    },
    methods: {
        addSkill() {
            this.allSkills.push(skillPrioritySelectize.getDefault());
            this.updateEdit(this.allSkills.length - 1);
        },
        clearData() {
            this.allSkills = [];
        },
        deleteSkill(idx) {
            this.allSkills.splice(idx, 1);
        },
        updateEdit(idx) {
            this.allSkills.forEach((skill, skillIdx) => {
                skill.isEdit = skillIdx === idx;
            });
        },
        getSkillPriorityLabel(skill) {
            return skillPriority.getPriorityLabel(skill);
        },
        getSkillLevelsCfg() {
            return Object.assign(
                skillLevelSelectize.getSkillLevelCfg(this.globalData.SKILL_LEVEL),
                {placeholder: 'All'}
            )
        },
        getSkillPriorityCfg() {
            return Object.assign(
                {},
                {...skillPrioritySelectize.cfg},
            );
        },
        getSkillSelectizeCfg() {
            return Object.assign(
                skillSelectize.getSkillCfg(this.initData.skills, {isMulti: false}),
                {placeholder: 'Select a skill'}
            );
        },
        setProjectSkillLevels(skill, skillLevelBits) {
            skill.skillLevelBits = skillLevelBits;
            skillLevelSelectize.setSkillLevels([skill]);
        },
        setSkillName(skill, skillId) {
            const targetSkill = this.initData.skills.find((s) => s.id === skillId);
            skill.id = skillId;
            skill.name = targetSkill.name;
        },
        setSkillPriority(skill, priority) {
            Object.assign(skill, skillPrioritySelectize.getPriorityValues(priority));
        },
        getSkills() {
            return this.allSkills.filter((s) => Boolean(s.id));  // Ignore any entries where the user didn't select a skill
        }
    },
    updated() {
        if (!this.skills) {
            return;
        }
        this.skills.forEach((s) => {
            const newSkill = dataUtil.deepCopy(s);  // Create a deep copy so we don't end up in infinite loop when updating skills
            this.allSkills.push(newSkill);
        })
        skillLevelSelectize.setSkillLevels(this.allSkills);
    }
}
</script>