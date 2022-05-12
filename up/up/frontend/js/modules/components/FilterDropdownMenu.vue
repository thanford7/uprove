<template>
    <div class="dropdown">
        <button class="btn btn-secondary dropdown-toggle" type="button" :id="elId"
                data-bs-toggle="dropdown" data-bs-auto-close="outside" aria-expanded="false">
            <i class="fas fa-filter"></i> Filters
            <div v-if="activeFilterCount" class="circle-counter -color-darkblue -color-white-text">
                {{activeFilterCount}}
            </div>
        </button>
        <ul class="dropdown-menu" :aria-labelledby="elId" :style="(isMobile) ? '' : 'min-width: 25vw;'">
            <li v-if="dropdownHeader">
                <h6 class="dropdown-header" style="font-weight: 900;">{{dropdownHeader}}</h6>
            </li>
            <slot></slot>
        </ul>
    </div>
</template>

<script>
import dataUtil from "../../utils/data";

export default {
    name: "FilterDropdownMenu",
    props: ['filters', 'dropdownHeader'],
    computed: {
        activeFilterCount() {
            return Object.values(this.filters).reduce((count, filter) => {
                if (!dataUtil.isEmptyOrNil(filter)) {
                    count++
                }
                return count
            }, 0);
        }
    },
    data() {
        return {
            elId: this.getNewElUid()
        }
    }
}
</script>