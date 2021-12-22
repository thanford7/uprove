<template>
    <table class="table table-borderless">
        <tr v-for="(item, idx) in listItems" :key="idx" class="align-top">
            <td>
                <font-awesome-layers class="fa-lg">
                    <font-awesome-icon icon="square" class="-color-darkblue-fa"/>
                    <font-awesome-layers-text transform="shrink-2" :value="idx + 1" style="color: white;" />
                </font-awesome-layers>
            </td>
            <td class="ps-2">
                {{item.main}}
                <div v-if="item.sub">{{item.sub}}</div>
            </td>
        </tr>
    </table>
</template>
<script>
export default {
    props: ['listItems']
}
</script>
