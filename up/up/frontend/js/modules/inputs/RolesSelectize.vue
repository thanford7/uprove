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
    props: ['roles', 'placeholder'],
    components: {InputSelectize},
    data() {
        return {
            targetEl: null,
            elSel: null
        }
    },
    computed: {
        rolesCfg() {
            const cfg = {
                plugins: ['remove_button'],
                maxItems: null,
                options: dataUtil.sortBy(this.roles.map((r) => ({value: r.id, text: r.name})), 'text')
            };
            return cfg;
        }
    },
    mounted() {
        this.targetEl = this.$refs.roles.targetEl;
        this.elSel = this.$refs.roles.elSel;
    }
}
</script>