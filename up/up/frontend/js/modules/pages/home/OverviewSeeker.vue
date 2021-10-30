<template>
    <div>
        <div v-if="isMobile" class="mb-2 pt-2 sticky-top -color-white">
            <button type="button" class="btn btn-sm btn-primary btn-full-width" @click="eventBus.$emit('open:something')">
                Request account
            </button>
        </div>
        <div v-if="!isMobile">
            <h2 class="d-inline-block">Job seekers</h2>
            <button type="button" class="btn btn-sm btn-primary d-inline-block -float-right" @click="eventBus.$emit('open:something')">
                Request account
            </button>
        </div>
        <h4>Build a portfolio of projects that makes your skill set stand out</h4>
        <ul class="list-table">
            <li>
                <font-awesome-icon :icon="['fas', 'plus-circle']" class="-color-darkblue-fa"/>&nbsp;
                <span class="-text-bold">Stand out</span>
                <div class="-sub-text pb-2">Demonstrate and showcase your skills that will make you stand out to employers in a way that no resume could.
                </div>
            </li>
            <li>
                <font-awesome-icon :icon="['fas', 'plus-circle']" class="-color-darkblue-fa"/>&nbsp;
                <span class="-text-bold">Save time</span>
                <div class="-sub-text pb-2">Complete a project for one potential employer and use it for all others that you plan to target. No more "one-off" project interviews for every employer.
                </div>
            </li>
            <li>
                <font-awesome-icon :icon="['fas', 'plus-circle']" class="-color-darkblue-fa"/>&nbsp;
                <span class="-text-bold">Be smart</span>
                <div class="-sub-text pb-2">Create multiple profiles targeted to unqiue employers or positions, see metrics on each of your profiles' performance, and get anonymous feedback from employers you interview with.
                </div>
            </li>
        </ul>
    </div>
</template>
<script>

export default {
}
</script>