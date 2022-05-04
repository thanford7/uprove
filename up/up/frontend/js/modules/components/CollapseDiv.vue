<template>
    <div>
        <div data-bs-toggle="collapse" :data-bs-target="`#${uid}`" :class="(isClosed) ? 'collapsed' : ''">
            <div style="display: inline-block">
                <slot name="header"/>
            </div>
            <i class="fas fa-angle-up fa-lg float-end pe-3"></i>
        </div>
        <div class="collapse" :id="uid" :class="(isClosed) ? '' : 'show'">
            <slot/>
        </div>
    </div>
</template>

<script>
export default {
    name: "CollapseDiv",
    props: ['elId', 'isClosed'],
    computed: {
        uid() {
            return `collapse-${this.elId}`;
        }
    }
}
</script>