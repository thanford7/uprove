<template>
    <div>
        <div class="row mt-3 mb-3">
            <div class="col-md-9">
                <h1>{{this.initData.project.title}} <span class="badge -color-darkblue">{{this.initData.project.function}}</span></h1>
                <div v-html="this.initData.project.description" class="-border-bottom--light mb-2"></div>
                <h3>Project brief</h3>
                <div v-html="this.initData.project.instructions" class="-border-bottom--light mb-2"></div>
                <div>
                    <h3>Files</h3>
                    <div v-for="file in this.initData.project.files">
                        <FileDisplay :file="file" :isIncludeDescription="true"/>
                    </div>
                </div>
            </div>
            <div class="col-md-3 sidebar">
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

export default {
    name: "ProjectPage.vue",
    components: {CandidateRequestAccountModal, EmployerRequestInfoModal, FileDisplay}
}
</script>