<template>
    <a href="#" @click="clickFn" class="-color-green-text"><i class="fas fa-plus-circle"></i>
        <span v-if="text">&nbsp;{{text}}</span>
        <slot></slot>
    </a>
</template>

<script>
export default {
    name: "AddNewLink",
    props: ['clickFn', 'text']
}
</script>