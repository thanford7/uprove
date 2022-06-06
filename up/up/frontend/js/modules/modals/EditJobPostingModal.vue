<template>
    <BaseModal
        :modalId="modalName"
        :modalTitle="(formData.id) ? 'Edit Customer Success posting': 'Create new Customer Success posting'"
        :primaryButtonText="(formData.id) ? 'Save changes' : 'Create posting'"
        :isLargeDisplay="true"
        :isScrollable="true"
        :isAllowDelete="Boolean(formData.id)"
        @saveChange="saveChange($event)"
        @deleteObject="deleteObject($event)"
    >
        <div class="mb-3">
            <label for="modalJobTitle" class="form-label">Job Title</label>
            <input type="text" class="form-control" placeholder="Required" id="modalJobTitle" v-model="formData.jobTitle">
        </div>
        <LocationInputs ref="locationInputs" :formData="formData"/>
        <div class="mb-3">
            <label for="modalJobDescription" class="form-label">Job Description</label>
            <InputWsiwyg
                ref="jobDescription"
                elId="modalJobDescription"
                placeholder="Add a description..."
                v-model="formData.jobDescription"
            />
        </div>
        <div class="mb-3">
            <label for="openDate" class="form-label">Open Date <InfoToolTip :content="TOOLTIPS.jobStartDate" :elId="getNewElUid()"/></label>
            <input type="date" class="form-control" id="openDate" v-model="formData.openDate">
            <span class="-sub-text">Leave blank for "DRAFT" status</span>
        </div>
        <div v-if="formData.id" class="mb-3">
            <label for="pauseDate" class="form-label">Pause Date <InfoToolTip :content="TOOLTIPS.jobPauseDate" :elId="getNewElUid()"/></label>
            <input type="date" class="form-control" id="pauseDate" v-model="formData.pauseDate">
        </div>
        <div v-if="formData.id" class="mb-3">
            <label for="closeDate" class="form-label">Close Date <InfoToolTip :content="TOOLTIPS.jobCloseDate" :elId="getNewElUid()"/></label>
            <input type="date" class="form-control" id="closeDate" v-model="formData.closeDate">
        </div>
    </BaseModal>
</template>

<script>
import {SEVERITY} from '../../globalData';
import BaseModal from "./BaseModal";
import form from "../../utils/form";
import InfoToolTip from "../components/InfoToolTip";
import InputSelectize from "../inputs/InputSelectize";
import InputWsiwyg from "../inputs/InputWsiwyg";
import LocationInputs from "../inputs/LocationInputs";
import $ from "jquery";

export default {
    name: "EditJobPostingModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    components: {
        BaseModal, InfoToolTip, InputSelectize, InputWsiwyg, LocationInputs,
    },
    data() {
        return {
            modalName: 'editJobPostingModal',
            crudUrl: 'job-posting/',
            isUpdateData: true,
            initDataKey: 'employer.jobs',
            requiredFields: {
                jobTitle: '#modalJobTitle',
                jobDescription: '#modalJobDescription',
            },
        }
    },
    methods: {
        processFormData() {
            return Object.assign(this.readForm(), {employerId: this.initData.employer.id})
        },
        onModalOpen() {
            if (form.isEmptyWysiwyg(this.formData?.jobDescription)) {
                this.$refs.jobDescription.addContent(customerSuccessJobDescription);
            }
        },
        setFormFields() {
            this.$refs.locationInputs.setStateVal(this.formData.stateId);
            this.$refs.locationInputs.setCountryVal(this.formData.countryId);
        },
        isGoodFormFields(formData) {
            if (form.isEmptyWysiwyg(formData.jobDescription)) {
                this.addPopover($('#modalJobDescription'),
                {severity: SEVERITY.WARN, content: 'Required field', isOnce: true}
                    );
                return false;
            }

            return true;
        },
    },
}

const customerSuccessJobDescription = [
    '<div><b>Job Responsibilities</b></div>',
    '<ul>',
    '<li>Own the entire customer journey for your customers with a deep understanding of their motivations, business drivers, strategic goals, and desired outcomes</li>',
    '<li>Develop and execute on detailed project plans to lead customers through implementation, change management, adoption, and value realization, unlocking growth and customer advocacy initiatives</li>',
    '<li>Become a product expert, advising your customers on how to best leverage our platform via best practices, for specific workflows, use cases, and learnings from other customers, etc.</li>',
    '<li>Quickly establish rapport and build relationships across all levels within a customer organization, including day-to-day IT contacts, influencers, and decision makers</li>',
    '<li>Work closely with cross functional teams across Product, Marketing, Account Management, external partners, etc. bringing them into the customer conversations as needed</li>',
    '<li>Advocate for and represent the voice of the customer to the rest of our organization</li>',
    '<li>Overcome obstacles and challenges independently and as part of the CS team. Solve problems for your customers, the team, and the company as we continue to grow</li>',
    '<li>Analyze customer usage trends and qualitative context to formulate hypothesis to articulate and demonstrate value to leadership and key stakeholders</li>',
    '<li>Upskill the broader CS team by mentoring junior CSMs, sharing best practices, and finding areas to optimize such as but not limited to existing processes and playbooks</li>',
    '<li>Identify upsell opportunities within your customer base and work with other internal teams to secure new business</li>',
    '</ul>'
].join('')
</script>