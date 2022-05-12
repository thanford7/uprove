<template>
    <InputSelectize
        ref="roles"
        :elId="getNewElUid()"
        :isParseAsInt="true"
        :cfg="rolesCfg"
        :placeholder="(placeholder) ? placeholder : 'Roles: All'"
    />
</template>

<script>
import InputSelectize from "./InputSelectize";
import dataUtil from "../../utils/data";

export default {
    name: "RolesSelectize",
    props: ['roleIds', 'placeholder'],
    components: {InputSelectize},
    data() {
        return {
            targetEl: null,
            elSel: null
        }
    },
    computed: {
        rolesCfg() {
            return {
                valueField: 'id',
                labelField: 'name',
                searchField: 'name',
                plugins: ['remove_button'],
                maxItems: null,
            };
        }
    },
    mounted() {
        this.targetEl = this.$refs.roles.targetEl;
        this.elSel = this.$refs.roles.elSel;
    },
    async created() {
        await this.loadData([{route: 'project-role/', dataKey: 'roles'}]);
        this.$refs.roles.resetOptions(this.cData.roles.filter((r) => !this.roleIds || this.roleIds.includes(r.id)));
    }
}
</script>