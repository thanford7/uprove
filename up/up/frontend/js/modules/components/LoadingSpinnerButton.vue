<template>
    <button class="btn spinner-btn" type="button" disabled>
      <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
      &nbsp;<span>{{msg}}</span>
    </button>
</template>

<script>
export default {
    name: "LoadingSpinnerButton",
    props: {
        msg: {
            type: String,
            default: 'Saving...'
        }
    }
}
</script>