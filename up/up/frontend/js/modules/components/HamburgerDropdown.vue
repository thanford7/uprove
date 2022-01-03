<template>
    <div class="dropdown hamburger-dropdown">
        <button class="btn btn-secondary dropdown-toggle no-caret" type="button" :id="elId"
                data-bs-toggle="dropdown" aria-expanded="false">
            <i class="fas fa-bars fa-1x"></i>
        </button>
        <ul class="dropdown-menu" :aria-labelledby="elId">
            <slot></slot>
        </ul>
    </div>
</template>

<script>
export default {
    name: "HamburgerDropdown",
    props: ['elId']
}
</script>