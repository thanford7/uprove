<template>
    <div>
        <div v-if="isMobile" class="mb-2 pt-2 sticky-top -color-white">
            <button type="button" class="btn btn-sm btn-primary btn-full-width" @click="eventBus.emit('open:employerRequestInfoModal')">
                Request demo
            </button>
        </div>
        <div v-if="!isMobile">
            <h2 class="d-inline-block">Employers</h2>
        </div>
        <h4>Get proof that candidates are the best fit by using project based interviews</h4>
        <ul class="list-table">
            <li>
                <font-awesome-icon :icon="['fas', 'plus-circle']" class="-color-darkblue-fa"/>&nbsp;
                <span class="-text-bold">Save time</span>
                <div class="-sub-text pb-2">Skip the time and hassle of preliminary rounds of interviews by reviewing candidates' projects, presentations, and answers to common interview
                    questions on your own time. Only interact with active candidates, knowing that candidates who have completed a project are not just "fishing" for job offers.
                </div>
            </li>
            <li>
                <font-awesome-icon :icon="['fas', 'plus-circle']" class="-color-darkblue-fa"/>&nbsp;
                <span class="-text-bold">Make the right hire</span>
                <div class="-sub-text pb-2">Use project based interviews that are similar to actual work to be confident that candidates are the best fit for the position.
                </div>
            </li>
            <li>
                <font-awesome-icon :icon="['fas', 'plus-circle']" class="-color-darkblue-fa"/>&nbsp;
                <span class="-text-bold">Leverage other companies</span>
                <div class="-sub-text pb-2">View anonymous notes and ratings from other companies that have interviewed the candidate.
                </div>
            </li>
        </ul>
    </div>
</template>
<script>

export default {

}
</script>