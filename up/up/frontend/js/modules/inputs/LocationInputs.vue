<template>
    <div>
        <div v-if="isIncludeRemote" class="mb-3">
            <label class="form-label">Location</label>
            <InputCheckBox
                :elId="getNewElUid()"
                label="Remote"
                :isActiveLabel="true"
                :isChecked="formData.isRemote"
                @click="formData.isRemote = $event"
            />
        </div>
        <div class="mb-3">
            <label :for="`${elId}-userCity`" class="form-label">City</label>
            <input type="text" class="form-control" placeholder="Optional" :id="`${elId}-userCity`" v-model="formData.city">
        </div>
        <div class="mb-3">
            <label class="form-label">State / Province / Region</label>
            <InputSelectize
                ref="userState"
                :elId="`${elId}-userState`"
                :isParseAsInt="true"
                placeholder="Optional"
                :cfg="{
                    maxItems: 1,
                    valueField: 'id',
                    labelField: 'name',
                    sortField: 'name',
                    searchField: 'name',
                    create: function(input) {
                        formData.state = input;
                    },
                    createOnBlur: true
                }"
                @selected="formData.stateId = $event"
            />
        </div>
        <div class="mb-3">
            <label class="form-label">Country</label>
            <InputSelectize
                ref="userCountry"
                :elId="`${elId}-userCountry`"
                :isParseAsInt="true"
                placeholder="Optional"
                :cfg="{
                    maxItems: 1,
                    valueField: 'id',
                    labelField: 'name',
                    sortField: 'name',
                    searchField: 'name',
                }"
                @selected="formData.countryId = $event"
            />
        </div>
    </div>
</template>

<script>
import InputCheckBox from "./InputCheckBox";
import InputSelectize from "./InputSelectize";

export default {
    name: "LocationInputs",
    props: ['formData', 'isIncludeRemote'],
    components: {
        InputCheckBox,
        InputSelectize
    },
    data() {
        return {
            elId: this.getNewElUid()
        }
    },
    methods: {
        setStateVal(stateId) {
            this.$refs.userState.elSel.setValue(stateId);
        },
        setCountryVal(countryId) {
            this.$refs.userCountry.elSel.setValue(countryId);
        }
    },
    async mounted() {
        await this.loadData([{route: 'locations/', dataKey: 'locations'}]);
        this.$refs.userState.resetOptions(this.cData.locations.states);
        this.$refs.userCountry.resetOptions(this.cData.locations.countries);
    }
}
</script>