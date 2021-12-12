<template>
    <div class="container-lg">
        <div class="row mt-3 mb-3" :class="(isMobile) ? 'mobile-top' : ''">
            <div class="col-md-9">
                <h1>{{this.initData.project.title}} <span class="badge -color-darkblue">{{this.initData.project.function}}</span></h1>
                <div v-html="this.initData.project.description" class="-border-bottom--light mb-2"></div>
                <h3>Project brief</h3>
                <div v-html="this.initData.project.background" class="-border-bottom--light mb-2"></div>
                <div>
                    <h3>Files</h3>
                    <div v-for="file in this.initData.project.files">
                        <FileDisplay :file="file" :isIncludeDescription="true" :isIncludeSkillLevels="true"/>
                    </div>
                </div>
            </div>
            <div class="col-md-3 sidebar mb-3">
                <div v-if="this.initData.project.isLimited">
                    <div class="-text-center">
                        Want to view the full project brief and files?
                    </div>
                    <div>
                        <span class="text-label text-label-sm">Employers</span>
                        <button type="button" class="btn btn-sm btn-primary w-100" @click="eventBus.emit('open:employerRequestInfoModal')">
                            Request demo
                        </button>
                    </div>
                    <div>
                        <span class="text-label text-label-sm">Job seekers</span>
                        <button type="button" class="btn btn-sm btn-primary w-100" @click="eventBus.emit('open:candidateRequestAccountModal')">
                            Request account
                        </button>
                    </div>
                </div>
                <div v-else>
                    <h4 class="-text-center">Customize project</h4>
                    <template v-if="isEmployer">
                        TODO: Hiring positions
                    </template>
                    <InputSelectize
                        ref="projectSkillLevels"
                        elId="projectSkillLevels"
                        :isParseAsBits="true"
                        placeholder="Skill level" :cfg="projectSkillLevelsCfg" @selected="pageData.skillLevelBits = $event"
                    />
                    <InputSelectize
                        ref="projectSkills"
                        elId="projectSkills"
                        :isParseAsInt="true"
                        placeholder="Project skills" :cfg="projectSkillsCfg" @selected="pageData.skillIds = $event"
                    />
                </div>
            </div>
        </div>
        <EmployerRequestInfoModal/>
        <CandidateRequestAccountModal/>
    </div>
</template>

<script>
import CandidateRequestAccountModal from "../../modals/CandidateRequestAccountModal";
import EmployerRequestInfoModal from "../../modals/EmployerRequestInfoModal";
import FileDisplay from "../../components/FileDisplay";
import InputSelectize from "../../inputs/InputSelectize";
import _ from "lodash";

export default {
    name: "ProjectPage.vue",
    components: {CandidateRequestAccountModal, EmployerRequestInfoModal, FileDisplay, InputSelectize},
    data() {
        return {
            pageData: {}
        }
    },
    computed: {
        projectSkillsCfg() {
            return {
                plugins: ['remove_button'],
                maxItems: null,
                options: _.sortBy(this.initData.skills.map((s) => ({value: s.id, text: s.skillName})), ['text'])
            };
        },
        projectSkillLevelsCfg() {
            return {
                maxItems: 1,
                options: Object.entries(this.globalData.SKILL_LEVEL).map(([key, txt]) => ({value: key, text: txt}))
            }
        }
    }
}
</script>