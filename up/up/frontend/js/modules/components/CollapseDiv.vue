<template>
    <div class="collapse-div">
        <div class="-color-darkblue -color-white-text p-0 d-flex align-items-center justify-content-between" data-bs-toggle="collapse" :data-bs-target="`#${uid}`" :class="(isClosed) ? 'collapsed' : ''">
            <div style="display: inline-block">
                <h6 class="ps-3 pe-3 pt-2 pb-2 m-0">
                    <slot name="header"/>
                </h6>
            </div>
            <i class="fas fa-angle-down fa-lg pe-3 -color-white-text"></i>
        </div>
        <div class="collapse pt-2 ps-3 pe-3" :id="uid" :class="(isClosed) ? '' : 'show'">
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