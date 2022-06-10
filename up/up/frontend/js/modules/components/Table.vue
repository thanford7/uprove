<template>
    <table class="table table-hover align-middle">
        <thead>
        <tr v-for="headerRow in headers">
            <th v-for="header in headerRow" :colspan="header.colspan" :class="header.classes">
                <template v-if="header.sortFn">
                    <span class="-anchor" @click="sortTable(header.sortFn, $event)">
                        {{ header.value }}
                    </span>
                    <span v-if="header.toolTip"> <InfoToolTip :content="header.toolTip" :elId="getNewElUid()"/></span>
                    <span class="sort-icon"></span>
                </template>
                <span v-else>
                    {{ header.value }}
                    <span v-if="header.toolTip"> <InfoToolTip :content="header.toolTip" :elId="getNewElUid()"/></span>
                </span>
            </th>
        </tr>
        </thead>
        <tbody>
        <slot name="body"/>
        <tr v-if="hasNoData && emptyDataMessage">
            <td :colspan="totalColspan"><span v-html="emptyDataMessage"></span></td>
        </tr>
        </tbody>
        <tfoot>
            <slot name="footer"/>
        </tfoot>
    </table>
</template>

<script>
import dataUtil from "../../utils/data";
import InfoToolTip from "./InfoToolTip";

export default {
    name: "Table",
    props: ['data', 'headers', 'emptyDataMessage'],
    components: {InfoToolTip},
    data() {
        return {
            sortKeys: [],
            sortIconAsc: '<i class="fas fa-sort-up"></i>',
            sortIconDesc: '<i class="fas fa-sort-down"></i>'
        }
    },
    computed: {
        hasNoData() {
            if (!this.data) {
                return true;
            }
            if (Array.isArray(this.data)) {
                return !Boolean(this.data.length);
            }
            return !Boolean(Object.keys(this.data).length)
        },
        totalColspan() {
            if (!this.headers) {
                return null;
            }
            return dataUtil.sum(this.headers[0].map((header) => header.colspan || 1));
        }
    },
    methods: {
        sortTable(sortKey, e) {
            let sortDirection = 1;
            const existingSortIndex = this.sortKeys.findIndex((sk) => sk.key === sortKey);
            if (existingSortIndex !== -1) {
                const [existingSort] = this.sortKeys.splice(existingSortIndex, 1);
                existingSort.direction *= -1;  // Change the sort direction
                this.sortKeys.unshift(existingSort);  // Move this sort key to the primary position
            } else {
                this.sortKeys.unshift(
                    {key: sortKey, direction: sortDirection, target: $(e.currentTarget).next('.sort-icon')}
                );
                // Only allow up to three sort rows at a time
                if (this.sortKeys.length > 3) {
                    this.sortKeys[3].target.html('')
                    this.sortKeys = this.sortKeys.slice(0, 3);
                }
            }
            this.sortKeys.forEach((sk, idx) => {
                const orderHtml = (sk.direction === 1) ? this.sortIconDesc : this.sortIconAsc;
                const sortTitle = (idx === 0) ? 'Primary sort' : (idx === 1) ? 'Secondary sort' : 'Tertiary sort'
                const sortHtml = `
                    <span class="fa-layers fa-fw" title="${sortTitle}">
                        ${orderHtml}
                        <span class="fa-custom-counter -color-moderategrey">${idx + 1}</span>
                    </span>
                `;
                sk.target.html(sortHtml);
            });

            dataUtil.sortBy(this.data, this.sortKeys, true);
        },
    }
}
</script>