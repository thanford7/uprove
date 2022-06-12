<template>
    <div :id="elId" class="btn btn-primary" :class="btnClasses" @click="saveChange" style="white-space: nowrap;">
        <i class="fas fa-bolt -color-yellow-text"></i>&nbsp; Fast apply
    </div>
</template>

<script>
import InfoToolTip from "../../components/InfoToolTip";
import {Popover} from "bootstrap";

export default {
    name: "FastApplyBtn",
    props: ['btnClasses', 'job'],
    components: {InfoToolTip},
    data() {
        return {
            elId: this.getNewElUid(),
            crudUrl: 'user-job-application/',
            pageRedirect: '/candidateDashboard/?tab=applications'
        }
    },
    methods: {
        readForm() {
            return {
                userId: this.globalData.uproveUser.id,
                employerJobId: this.job.id
            }
        },
        initTooltip() {
            const el$ = $(`#${this.elId}`);
            if (!this.popover && el$.length) {
                let container = 'body';
                const modalParent = el$.parents('.modal');
                if (modalParent.length) {
                    container = `#${$(modalParent[0]).attr('id')}`;
                }
                this.popover = new Popover(el$, {
                    content: 'This employer accepts Uprove profiles for a job application. Apply with a single click!',
                    html: false,
                    container,
                    placement: 'auto',
                    trigger: 'hover'
                });
            }
        }
    },
    mounted() {
        this.initTooltip();
    },
    updated() {
        this.initTooltip();
    }
}
</script>