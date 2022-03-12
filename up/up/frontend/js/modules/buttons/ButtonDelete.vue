<template>
    <button type="button" class="btn btn-danger" :class="(isSmall) ? 'btn-sm' : ''" title="Delete">
        <i class="fas fa-trash -color-white-text"></i>
    </button>
</template>

<script>
export default {
    name: "ButtonDelete",
    props: ['isSmall']
}
</script>