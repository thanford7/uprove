<template>
    <Table :data="allTags" :headers="headers">
        <template v-slot:body>
            <template v-for="(tag, idx) in allTags">
                <tr v-if="!tag.isEdit" @click="updateEdit(idx)">
                    <td>{{tag.title}}</td>
                    <td>{{tag.description}}</td>
                    <td><i class="fas fa-trash -color-red-text" @click="deleteTag(idx)" :title="`Remove ${tag.tagType}`"></i></td>
                </tr>
                <template v-else>
                    <tr>
                        <td class="border-bottom-0">
                            <InputSelectize
                                ref="tag"
                                :cfg="getTagSelectizeCfg(tag)"
                                :elId="getNewElUid()"
                                :items="tag.id"
                                @selected="setTag(tag, $event)"
                            />
                        </td>
                        <td class="border-bottom-0"></td>
                        <td class="border-bottom-0">
                            <i class="fas fa-check-square -color-green-text" @click="updateEdit(-1)"></i>
                        </td>
                    </tr>
                    <tr>
                        <td :colspan="headers[0].length" class="border-top-0">
                            <textarea
                                rows="3" class="form-control"
                                placeholder="Description (max 200 characters)"
                                maxlength="200"
                                v-model="tag.description"
                            />
                        </td>
                    </tr>
                </template>
            </template>
        </template>
        <template v-slot:footer>
            <a v-if="tagType !== tagTypes.SKILL || allTags.length <= skillLimit" href="#" @click="addTag">
                <i class="fas fa-plus -color-green-text"></i> Add {{tagType}}
            </a>
            <div v-else>
                Skill limit of {{skillLimit}} met
                <InfoToolTip :elId="getNewElUid()" content="Skills are limited to make sure that the most relevant ones are displayed to employers"/>
            </div>
        </template>
    </Table>
</template>

<script>
import {TAG_TYPES} from '../../globalData';
import BadgesSkillLevels from "./BadgesSkillLevels";
import dataUtil from "../../utils/data";
import InfoToolTip from "./InfoToolTip";
import InputSelectize from "../inputs/InputSelectize";
import skillLevelSelectize from "../selectizeCfgs/skillLevels";
import SkillLevelsSelectize from "../inputs/SkillLevelsSelectize";
import Table from "./Table";
import tagSelectize from "../selectizeCfgs/tag";

export default {
    name: "EditUserTagTable",
    components: {BadgesSkillLevels, InfoToolTip, InputSelectize, SkillLevelsSelectize, Table},
    props: ['userTags', 'tagType'],
    data() {
        return {
            headers: this.getHeaders(),
            allTags: [],
            tagTypes: TAG_TYPES,
            skillLimit: 5
        }
    },
    watch: {
        userTags(newVal) {
            this.setAllTags();
        }
    },
    methods: {
        addTag() {
            this.allTags.push({type: this.tagType});
            this.updateEdit(this.allTags.length - 1);
        },
        clearData() {
            this.allTags = [];
        },
        deleteTag(idx) {
            this.allTags.splice(idx, 1);
        },
        getHeaders() {
            const headers = [{value: 'Description', classes: 'w-50'}, {}];
            if (this.tagType === TAG_TYPES.INTEREST) {
                headers.unshift({value: dataUtil.capitalize(TAG_TYPES.INTEREST)});
            } else if (this.tagType === TAG_TYPES.SKILL) {
                headers.unshift(
                    {value: dataUtil.capitalize(TAG_TYPES.SKILL)},
                );
            }
            return [headers];
        },
        updateEdit(idx) {
            this.allTags.forEach((tag, tagIdx) => {
                tag.isEdit = tagIdx === idx;
            });
        },
        getTagSelectizeCfg(initialItems) {
            return Object.assign(
                tagSelectize.getTagCfg(this.tagType, {isMulti: false}),
                {options: [initialItems]}
            );
        },
        setTag(tag, tagId) {
            tag.id = parseInt(tagId) || tagId;
            // If ID is not an integer, that means it's a new tag
            if (!parseInt(tagId)) {
                tag.title = tagId;
            } else {
                tag.title = this.getTagById(tagId).title;
            }
        },
        getTags() {
            return this.allTags
                .filter((t) => Boolean(t.id))  // Ignore any entries where the user didn't select a tag
                .map((t) => {
                    // Remove ID for new tags
                    if (!parseInt(t.id)) {
                        t.id = null;
                    }
                    t.isEdit = false;  // Close the edit form if it is currently open
                    return t;
                });
        },
        getTagById(tagId) {
            return this.$refs.tag.elSel.options[tagId] || {}
        },
        hasDuplicate() {
            const tags = this.getTags();
            const usedTags = new Set();
            for(let i = 0; i < tags.length; i++) {
                const tag = tags[i].title;
                if (usedTags.has(tag)) {
                    return true;
                } else {
                    usedTags.add(tag);
                }
            }
            return false;
        },
        setAllTags() {
            this.allTags = [];
            (this.userTags || []).forEach((ut) => {
                this.allTags.push({
                    type: ut.tagType,
                    id: ut.tagId,
                    description: ut.description,
                    title: ut.title
                });
            });
            skillLevelSelectize.setSkillLevels(this.allTags, true);
        }
    },
    mounted() {
        this.setAllTags();
    },
}
</script>