<template>
    <div v-if="contentItem">
        <div class="card-body pt-1 pb-1">
            <BadgesSkillLevels :skillLevels="contentItem.customProject.skillLevels"/>
            <BadgesSkills :skills="contentItem.customProject.skills"/>
            <div v-html="contentItem.customProject.projectDescription"></div>
        </div>
    </div>
</template>

<script>
import BadgesSkillLevels from "../../components/BadgesSkillLevels";
import BadgesSkills from "../../components/BadgesSkills";
import FileDisplay from "../../components/FileDisplay";
import form from "../../../utils/form";
import skillLevels from "../../selectizeCfgs/skillLevels";

export default {
    name: "ContentProject",
    components: {BadgesSkillLevels, BadgesSkills, FileDisplay},
    props: {
        contentItem: Object
    },
    methods: {
        hasText(text) {
            return !form.isEmptyWysiwyg(text);
        },
        updateSkillLevels() {
            if (!this.contentItem.customProject.skillLevels) {
                skillLevels.setSkillLevels([this.contentItem.customProject], true);
            }
        }
    },
    mounted() {
        this.updateSkillLevels();
    },
    updated() {
        this.updateSkillLevels();
    }
}
</script>