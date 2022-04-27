<template>
    <div class="card-custom">
        <BasePage :headerTitle="`${initData.employer.companyName}: Uprove Assessment Configuration`"
                  :headerImage="initData.employer.logo">
            <div v-if="!isMsgSent">
                <div class="row mb-3">
                    <div>
                        <h5>Assessment for {{ initData.candidate.name }} ({{ initData.jobTitle }} position)</h5>
                    </div>
                    <div class="mb-3 col-md-4">
                        <label class="form-label">
                            Candidate Email Address
                            <InfoToolTip :elId="getNewElUid()"
                                         content="To send to multiple email addresses, separate each email address with a comma"/>
                        </label>
                        <input id="candidateEmails" type="text" class="form-control" placeholder="Required"
                               v-model="initData.candidate.emails">
                    </div>
                    <div class="mb-3 col-md-4">
                        <label class="form-label">
                            {{ initData.employer.companyName }} Contact Email Address
                            <InfoToolTip :elId="getNewElUid()"
                                         content="This is the individual that the candidate should reach out to if they have questions or issues"/>
                        </label>
                        <InputSelectize
                            ref="companyContactEmail"
                            elId="companyContactEmail"
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
                            placeholder="Required"
                            @selected="setCompanyContactEmail"
                        />
                    </div>
                    <div class="mb-3 col-md-4">
                        <label class="form-label">
                            {{ initData.employer.companyName }} Contact Name
                            <InfoToolTip :elId="getNewElUid()"
                                         content="This is the individual that the candidate should reach out to if they have questions or issues"/>
                        </label>
                        <InputSelectize
                            ref="companyContactName"
                            elId="companyContactName"
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
                            placeholder="Required"
                            @selected="setCompanyContactName"
                        />
                    </div>
                    <div class="mb-3 col-md-6">
                        <label class="form-label">
                            Assessment
                            <InfoToolTip :elId="getNewElUid()"
                                         content="This is the project assessment that the candidate must complete. You can open any of the assessments to get more details"/>
                        </label>
                        <ProjectsSelectize
                            ref="customProject"
                            :employerId="initData.employer.id"
                            :allowedProjects="selectedProject"
                            @projectChange="formData.customProject = $event"
                        />
                    </div>
                    <div class="mb-3 col-md-6">
                        <ProjectConfigSelectize
                            v-if="formData.customProject"
                            ref="customProjectCfg"
                            :employerId="initData.employer.id"
                            :customProject="formData.customProject"
                            :project="getProject(formData.customProject)"
                        />
                    </div>
                </div>
                <div class="row mb-2">
                    <div class="mb-3 col-12">
                        <label class="form-label">
                            Assessment Email To Candidate
                            <InfoToolTip :elId="getNewElUid()"
                                         content="This email will be sent to give the candidate instructions on how to complete the assessment. You can modify the language as you see fit"/>
                        </label>
                        <p class="-text-medium">From: {{ formData.companyContactEmail }}</p>
                        <p class="-text-medium">CC: {{ globalData.CANDIDATE_SUPPORT_EMAIL }}</p>
                        <p class="-text-medium">To:
                            {{ (initData.candidate.emails && Array.isArray(initData.candidate.emails)) ? initData.candidate.emails.join('; ') : initData.candidate.emails }}</p>
                        <div class="mb-3">
                            <span class="-text-medium">Subject:&nbsp;</span>
                            <input
                                id="assessmentEmailTitle"
                                type="text" class="form-control w-75"
                                placeholder="Email subject" v-model="assessmentEmailTitle"
                                style="display: inline-block;"
                            >
                        </div>
                        <InputWsiwyg :elId="assessmentEmail" v-model="assessmentEmail"/>
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col-12 btn btn-primary" @click="saveChange">
                        <i class="fas fa-paper-plane"></i> Send assessment email
                    </div>
                </div>
            </div>
        </BasePage>
    </div>
</template>

<script>
import BasePage from "../base/BasePage";
import customProjectUtil from "../../../utils/customProject";
import InfoToolTip from "../../components/InfoToolTip";
import InputSelectize from "../../inputs/InputSelectize";
import InputWsiwyg from "../../inputs/InputWsiwyg";
import ProjectConfigSelectize from "../../inputs/ProjectConfigSelectize";
import ProjectsSelectize from "../../inputs/ProjectsSelectize";
import globalData, {SEVERITY} from "../../../globalData";

export default {
    name: "LeverSendOpportunityPage",
    components: {BasePage, InfoToolTip, InputSelectize, InputWsiwyg, ProjectConfigSelectize, ProjectsSelectize},
    data() {
        return {
            crudUrl: 'lever/send-assessment/',
            requiredFields: {
                candidateEmails: '#candidateEmails',
                companyContactEmail: '#companyContactEmail',
                companyContactName: '#companyContactName',
                customProject: null
            },
            isMsgSent: false
        }
    },
    computed: {
        assessmentEmail() {
            const projectUrl = `${this.globalData.BASE_URL}/job-posting/${this.initData.jobId}/`;
            return `
                <p>Hi ${this.initData.candidate.name},</p>
                <p>Congratulations on making it to this stage in the interview process with
                ${this.initData.employer.companyName} for the ${this.initData.jobTitle} position! The next step
                in the process is to complete a case study. The background, instructions, and supporting files
                can be accessed using
                <a id="redirectLink" href="${projectUrl}">this link</a>.
                If you do not already have an account with Uprove, you will be asked to set a password before continuing to the
                case study. If you have any questions about the case study, you can email
                <a href="mailto: ${globalData.CANDIDATE_SUPPORT_EMAIL}">${globalData.CANDIDATE_SUPPORT_EMAIL}</a>.
                If you have any questions about ${this.initData.employer.companyName} or the interview process, please email me.
                </p>
                <p>Sincerely,</p>
                <p>${this.formData.companyContactName}</p>
            `;
        },
        assessmentEmailTitle() {
            return `${this.initData.employer.companyName} | Interview next steps for ${this.initData.jobTitle} position`;
        },
        selectedProject() {
            if (this.formData.customProject) {
                return [this.formData.customProject];
            }
            return (initData.primaryCustomProject) ? [initData.primaryCustomProject] : [];
        }
    },
    methods: {
        getSuccessMessage() {
            const emails = (Array.isArray(this.initData.candidate.emails)) ? this.initData.candidate.emails.join('; ') : this.initData.candidate.emails;
            return `Message successfully sent to ${emails}. You can close this page now.`;
        },
        getAjaxCfgOverride() {
            return {
                method: 'POST'
            };
        },
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
        readForm() {
            return Object.assign({}, this.formData, {
                candidateName: this.initData.candidate.name,
                candidateEmails: this.initData.candidate.emails,
                emailTitle: this.assessmentEmailTitle,
                emailBody: this.assessmentEmail,
                employerId: this.initData.employer.id,
                jobId: this.initData.jobId,
                opportunityId: this.initData.candidate.opportunityId
            });
        },
        isGoodFormFields(formData) {
            if (!formData.customProject.skillLevelBit) {
                this.addPopover($(this.$refs.customProjectCfg.getSkillLevelTargetEl()),
                    {severity: SEVERITY.WARN, content: 'You must select a skill level', isOnce: true}
                );
                return false;
            }
            if (!formData.emailBody.includes('redirectLink')) {
                this.addPopover($('#assessmentEmail'),
                    {severity: SEVERITY.WARN, content: 'Email must contain a link to the assessment', isOnce: true}
                );
                return false;
            }
            if (!formData.emailTitle) {
                this.addPopover($('#assessmentEmailTitle'),
                    {severity: SEVERITY.WARN, content: 'Email title cannot be blank', isOnce: true}
                );
                return false;
            }
            return true;
        }
    },
    mounted() {
        const companyContacts = this.initData.candidate.contacts;
        if (companyContacts.length) {
            this.$refs.companyContactEmail.elSel.setValue(companyContacts[0].email, true);
            this.$refs.companyContactName.elSel.setValue(companyContacts[0].name, true);
            this.formData.companyContactEmail = companyContacts[0].email;
            this.formData.companyContactName = companyContacts[0].name;
        }
        this.formData.customProject = this.initData.primaryCustomProject;
        if (this.formData.customProject) {
            this.formData.customProject.skillIds = this.formData.customProject.skills.map((s) => s.id);
        }
        this.requiredFields.customProject = this.$refs.customProject.getTargetEl();

        this.eventBus.on('ajaxSuccess', () => {
            this.isMsgSent = true;
        });
    }
}
</script>