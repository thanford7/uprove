<template>
    <Table :data="allSkills" :headers="headers">
        <template v-slot:body>
            <template v-for="(skill, idx) in allSkills">
                <tr v-if="!skill.isEdit" @click="updateEdit(idx)">
                    <td>{{skill.name}}</td>
                    <td>{{skill.instruction}}</td>
                    <td><i class="fas fa-trash -color-red-text" @click="deleteSkill(idx)" title="Remove skill"></i></td>
                </tr>
                <template v-else>
                    <tr>
                        <td class="border-bottom-0">
                            <SkillsSelectize
                                v-if="!skill.projectId"
                                :skills="initData.skills"
                                :cfg="{isMulti: false, isShowRequired: true, placeholder: 'Select a skill'}"
                                :items="skill.id"
                                @selected="setSkill(skill, $event)"
                            />
                            <span v-else>{{skill.name}}</span>
                        </td>
                        <textarea
                            rows="3" class="form-control"
                            placeholder="Description"
                            v-model="skill.instruction"
                        />
                        <td class="border-bottom-0">
                            <i class="fas fa-check-square -color-green-text" @click="updateEdit(-1)"></i>
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
import SkillLevelsSelectize from "../inputs/SkillLevelsSelectize";
import SkillsSelectize from "../inputs/SkillsSelectize";
import Table from "./Table";

export default {
    name: "EditSkillsTable",
    components: {BadgesSkillLevels, InputSelectize, SkillLevelsSelectize, SkillsSelectize, Table},
    props: ['skills'],
    data() {
        return {
            headers: [[{value: 'Name'}, {value: 'Description'}, {}]],
            allSkills: []
        }
    },
    methods: {
        addSkill() {
            this.allSkills.push({});
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
        setSkill(skill, skillId) {
            const targetSkill = this.initData.skills.find((s) => s.id === skillId);
            skill.id = skillId;
            Object.assign(skill, dataUtil.pick(targetSkill, ['name', 'instruction']));
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
    }
}
</script>