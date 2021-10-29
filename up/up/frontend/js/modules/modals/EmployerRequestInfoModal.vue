<template>
    <BaseModal
        modalId="employerRequestInfoModal"
        modalTitle="Request information"
        headerSubtext="Once you submit the form, we'll email you additional information and find a time to demo the platform"
        primaryButtonText="Send me info"
        @saveChange="saveChange"
    >
        <div class="mb-3">
            <label for="formEmployerRequestFName" class="form-label">First Name</label>
            <input type="text" class="form-control" placeholder="Required" id="formEmployerRequestFName" v-model="formData.firstName">
        </div>
        <div class="mb-3">
            <label for="formEmployerRequestLName" class="form-label">Last Name</label>
            <input type="text" class="form-control" placeholder="Required" id="formEmployerRequestLName" v-model="formData.lastName">
        </div>
        <div class="mb-3">
            <label for="formEmployerRequestCName" class="form-label">Company Name</label>
            <input type="text" class="form-control" placeholder="Required" id="formEmployerRequestCName" v-model="formData.companyName">
        </div>
        <div class="mb-3">
            <label for="formEmployerRequestEmail" class="form-label">Email</label>
            <InputEmail elId="formEmployerRequestEmail" placeholder="Required" v-model="formData.fromEmail"/>
        </div>
        <div class="mb-3">
            <label for="formEmployerRequestTitle" class="form-label">Your Title</label>
            <input type="text" class="form-control" placeholder="Required" id="formEmployerRequestTitle" v-model="formData.title">
        </div>
        <div class="mb-3">
            <label for="formEmployerRequestCoSize" class="form-label">Company Employee Count</label>
            <InputSelectize
                elId="formEmployerRequestCoSize"
                placeholder="Optional" :cfg="coSizeCfg" @selected="formData.size = $event"/>
        </div>
        <div class="mb-3">
            <label for="formEmployerRequestFunctions" class="form-label">Functions You're Hiring</label>
            <InputSelectize
                elId="formEmployerRequestFunctions"
                placeholder="Optional" :cfg="functionsCfg" @selected="formData.roleFunctions = $event"/>
        </div>
        <div>
            <label for="formEmployerRequestSkills" class="form-label">Skills You're Hiring</label>
            <InputSelectize
                elId="formEmployerRequestSkills"
                placeholder="Optional" :cfg="skillsCfg" @selected="formData.roleSkills = $event"/>
        </div>
        <div>
            <label for="formEmployerRequestNote" class="form-label">Note</label>
            <textarea
                rows="3" class="form-control"
                placeholder="Any other questions or information you want to share..."
                id="formEmployerRequestNote"
                v-model="formData.note"
            />
        </div>
    </BaseModal>
</template>

<script>
import Modal from 'bootstrap/js/dist/modal';
import {mapState} from 'vuex';
import BaseModal from './BaseModal.vue';
import InputEmail from "../inputs/InputEmail";
import InputSelectize from "../inputs/InputSelectize";
import mainData from "../../mainData";

export default {
    name: "EmployerRequestInfoModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal, InputEmail, InputSelectize},
    data() {
        return {
            modal$: null,
            crudUrl: 'email/',
            formData: {},
            coSizeCfg: {
                maxItems: 1,
                options: [
                    {value: '1-10', text: '1-10'},
                    {value: '11-50', text: '11-50'},
                    {value: '51-100', text: '51-100'},
                    {value: '101-250', text: '101-250'},
                    {value: '251-500', text: '101-250'},
                    {value: '501-1000', text: '501-1000'},
                    {value: '1001+', text: '1001+'},
                ]
            },
            functionsCfg: {
                maxItems: null,
                options: Object.entries(mainData.SUPPORTED_FUNCTIONS).map(([key, txt]) => ({value: key, text: txt}))
            },
            skillsCfg: {
                maxItems: null,
                options: Object.entries(mainData.SUPPORTED_SKILLS).map(([key, txt]) => ({value: key, text: txt}))
            }
        }
    },
    computed: {
        ...mapState({
            eventBus: 'eventBus'
        }),
    },
    methods: {
        hookEvents() {
            this.eventBus.on('open:employerRequestInfoModal', () => {
                this.modal$.show();
            });
        },
        readForm() {
            return {
                ...this.formData,
                type: mainData.EMAIL_EMPLOYER_INTEREST,
                subject: 'Employer interest'
            };
        },
        saveChange() {
            this.superSaveChange({method: 'POST'})
        }
    },
    mounted() {
        if (!this.modal$) {
            this.modal$ = new Modal($('#employerRequestInfoModal'));
        }
    }
}
</script>