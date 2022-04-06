<template>
    <div class="row mt-3">
        <div class="card-custom card-custom--no-side-margin filter ps-4 pe-4">
            <slot/>
        </div>
    </div>
</template>

<script>
export default {
    name: "BaseFilter"
}
</script>