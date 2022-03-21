<template>
    <ul class="fa-ul">
        <li v-for="item in items">
            <span class="fa-li">
            <i :class="imageClasses"></i></span>
            {{item}}
        </li>
    </ul>
</template>

<script>
export default {
    name: "ListFontAwesome",
    props: ['faClassesStr', 'faColor', 'items'],
    computed: {
        imageClasses() {
            let str = this.faClassesStr;
            if (this.faColor) {
                str += ` -color-${this.faColor}-text`;
            }
            return str;
        }
    }
}
</script>