<template>
    <div class="card-custom">
        <BasePage :headerTitle="`${initData.employer.companyName}: Uprove Assessment Configuration`" :headerImage="initData.employer.logo">
            <div class="row mb-3">
                <div>
                    <h5>Assessment for {{initData.candidate.name}}</h5>
                </div>
                <div class="mb-3 col-md-4">
                    <label class="form-label">
                        Candidate email address
                        <InfoToolTip :elId="getNewElUid()" content="To send to multiple email addresses, separate each email address with a comma"/>
                    </label>
                    <input type="text" class="form-control" placeholder="Required" v-model="initData.candidate.emails">
                </div>
                <div class="mb-3 col-md-4">
                    <label class="form-label">
                        {{initData.employer.companyName}} contact email address
                        <InfoToolTip :elId="getNewElUid()" content="This is the individual that the candidate should reach out to if they have questions or issues"/>
                    </label>
                    <InputSelectize
                        ref="companyContactEmail"
                        :elId="getNewElUid()"
                        :cfg="{
                            maxItems: 1,
                            create: true,
                            persist: false,
                            hideSelected: true,
                            options: initData.candidate.contacts,
                            valueField: 'email',
                            labelField: 'email',
                            searchField: ['email']
                        }"
                        placeholder="Optional"
                        @selected="setCompanyContactEmail"
                    />
                </div>
                <div class="mb-3 col-md-4">
                    <label class="form-label">
                        {{initData.employer.companyName}} contact name
                        <InfoToolTip :elId="getNewElUid()" content="This is the individual that the candidate should reach out to if they have questions or issues"/>
                    </label>
                    <InputSelectize
                        ref="companyContactName"
                        :elId="getNewElUid()"
                        :cfg="{
                            maxItems: 1,
                            create: true,
                            persist: false,
                            hideSelected: true,
                            options: initData.candidate.contacts,
                            valueField: 'name',
                            labelField: 'name',
                            searchField: ['name']
                        }"
                        placeholder="Optional"
                        @selected="setCompanyContactName"
                    />
                </div>
                <div class="mb-3 col-md-6">
                    <label class="form-label">
                        Assessment
                        <InfoToolTip :elId="getNewElUid()" content="This is the project assessment that the candidate must complete. You can open any of the assessments to get more details"/>
                    </label>
                    <ProjectsSelectize
                        :employerId="initData.employer.id"
                        @projectChange="formData.customProject = $event"
                    />
                </div>
                <div class="mb-3 col-md-6">
                    <ProjectConfigSelectize
                        v-if="formData.customProject"
                        :employerId="initData.employer.id"
                        :customProject="formData.customProject"
                        :project="getProject(formData.customProject)"
                    />
                </div>
            </div>
            <div class="row mb-3">
                <div class="mb-3 col-md-6">
                    <label class="form-label">
                        Assessment email to candidate
                        <InfoToolTip :elId="getNewElUid()" content="This email will be sent to give the candidate instructions on how to complete the assessment. You can modify the language as you see fit"/>
                    </label>
                    <InputWsiwyg :elId="getNewElUid()" v-model="assessmentEmail"/>
                </div>
            </div>
        </BasePage>
    </div>
</template>

<script>
import BasePage from "../base/BasePage";
import InfoToolTip from "../../components/InfoToolTip";
import InputSelectize from "../../inputs/InputSelectize";
import InputWsiwyg from "../../inputs/InputWsiwyg";
import ProjectConfigSelectize from "../../inputs/ProjectConfigSelectize";
import ProjectsSelectize from "../../inputs/ProjectsSelectize";

export default {
    name: "LeverSendOpportunityPage",
    components: {BasePage, InfoToolTip, InputSelectize, InputWsiwyg, ProjectConfigSelectize, ProjectsSelectize},
    computed: {
        assessmentEmail() {
            return `
                <p>Hi ${this.initData.candidate.name},</p>
                <p>Congratulations on making it to this stage in the interview process! The next step in the process
                is to complete a case study. The background, instructions, and supporting files can be accessed using
                <a href="#">this link</a>
                </p>
            `
        }
    },
    methods: {
        getProject(customProject) {
            if (!customProject) {
                return null;
            }
            return this.initData.projects.find((p) => p.id === customProject.projectId);
        },
        setCompanyContactName(name) {
            this.formData.companyContactName = name;
            const contact = this.initData.candidate.contacts.find((c) => c.name === name);
            if (contact) {
                this.$refs.companyContactEmail.elSel.setValue(contact.email, true);
                this.formData.companyContactEmail = contact.email;
            }
        },
        setCompanyContactEmail(email) {
            this.formData.companyContactEmail = email;
            const contact = this.initData.candidate.contacts.find((c) => c.email === email);
            if (contact) {
                this.$refs.companyContactName.elSel.setValue(contact.name, true);
                this.formData.companyContactName = contact.name;
            }
        },
    },
    mounted() {
        const companyContacts = this.initData.candidate.contacts;
        if (companyContacts.length === 1) {
            this.$refs.companyContactEmail.elSel.setValue(companyContacts[0].email, true);
            this.$refs.companyContactName.elSel.setValue(companyContacts[0].name, true);
            this.formData.companyContactEmail = companyContacts[0].email;
            this.formData.companyContactName = companyContacts[0].name;
        }
    }
}
</script>