<template>
    <input
        type="email"
        class="form-control"
        pattern=".+@.+\..+"
        :id="elId || _uid"
        :placeholder="placeholder"
        :value="modelValue"
        @change="$emit('update:modelValue', $event.target.value)"
    >
</template>

<script>
export default {
    name: 'InputEmail.vue',
    props: ['elId', 'placeholder', 'modelValue'],
}
</script>