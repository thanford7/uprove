<template>
    <table class="table table-borderless">
        <tr v-for="(item, idx) in listItems" :key="idx" class="align-top">
            <td>
                {{idx+1}}
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
