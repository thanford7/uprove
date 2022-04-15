<template>
    <div class="card-custom">
        <BasePage :headerTitle="`${initData.employer.companyName}: Uprove Assessment Configuration`" :headerImage="initData.employer.logo">
            <div class="row">
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
            </div>
        </BasePage>
    </div>
</template>

<script>
import BasePage from "../base/BasePage";
import InfoToolTip from "../../components/InfoToolTip";
import InputSelectize from "../../inputs/InputSelectize";

export default {
    name: "LeverSendOpportunityPage",
    components: {BasePage, InfoToolTip, InputSelectize},
    methods: {
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