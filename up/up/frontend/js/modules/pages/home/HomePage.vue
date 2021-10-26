<template>
    <div id="vue-container" class="container-fluid">
        <div class="row mt-4">
            <div class="col-12">
                <h3 class="-text-center -color-moderategrey-text"><em>A picture is worth 1,000 words; A project is worth 1,000 resumes</em></h3>
            </div>
        </div>
        <div class="desktop-only">
            <div class="row mt-4">
                <div class="col-md-6 pb-2">
                    <OverviewEmployer/>
                </div>
                <div class="col-md-6 pb-2 -border-left--light">
                    <OverviewSeeker/>
                </div>
            </div>
            <div class="row">
                <div class="col-md-6 mb-2 pb-2">
                    <h4>How it works</h4>
                    <OrderedList :listItems="employerHowItWorks"/>
                </div>
                <div class="col-md-6 mb-2 pb-2 -border-left--light">
                    <h4>How it works</h4>
                    <OrderedList :listItems="seekerHowItWorks"/>
                </div>
            </div>
        </div>
        <div class="mobile-only">
            <ul class="nav nav-tabs" id="viewerTypeTabs" role="tablist">
                <li class="nav-item" role="presentation">
                    <button class="nav-link active" id="employer-tab" data-bs-toggle="tab" data-bs-target="#employer" type="button" role="tab" aria-controls="employer" aria-selected="true">Employers</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="seeker-tab" data-bs-toggle="tab" data-bs-target="#seeker" type="button" role="tab" aria-controls="job seeker" aria-selected="false">Job seekers</button>
                </li>
            </ul>
            <div class="tab-content" id="viewerTypeContent">
                <div class="tab-pane fade show active" id="employer" role="tabpanel" aria-labelledby="employer-tab">
                    <div class="col-12 pb-2">
                        <OverviewEmployer :isMobile="true"/>
                    </div>
                    <div class="col-12 mb-2 pb-2">
                        <h4>How it works</h4>
                        <OrderedList :listItems="employerHowItWorks"/>
                    </div>
                </div>
                <div class="tab-pane fade" id="seeker" role="tabpanel" aria-labelledby="seeker-tab">
                    <div class="col-12 pb-2">
                        <OverviewSeeker :isMobile="true"/>
                    </div>
                    <div class="col-12 mb-2 pb-2">
                        <h4>How it works</h4>
                        <OrderedList :listItems="seekerHowItWorks"/>
                    </div>
                </div>
            </div>
        </div>
        <EmployerRequestInfoModal/>
    </div>
</template>
<script>
import EmployerRequestInfoModal from "../../modals/EmployerRequestInfoModal";
import OrderedList from '../../components/OrderedList.vue';
import OverviewEmployer from './OverviewEmployer.vue';
import OverviewSeeker from './OverviewSeeker.vue';

export default {
    components: {EmployerRequestInfoModal, OrderedList, OverviewEmployer, OverviewSeeker},
    data() {
        return {
            employerHowItWorks: [
                {
                    main: 'Pick one or more positions to create job openings'
                },
                {
                    main: 'Select from a catalogue of projects that demonstrate skills for the specified positions'
                },
                {
                    main: 'Optionally add common interview screening questions (e.g. What interests you in this position?)'
                },
                {
                    main: 'Review and select candidates that have completed the project and screening questions'
                },
                {
                    main: 'Schedule any additional interviews you want candidates to complete'
                },
                {
                    main: 'Extend an offer!'
                },
            ],
            seekerHowItWorks: [
                {
                    main: 'Pick one or more positions you want to be hired for'
                },
                {
                    main: 'Optionally select the types of employers (e.g. size, industry, geography) and specific employers you want to work for'
                },
                {
                    main: 'Complete one or more projects that are used by employers to identify candidates'
                },
                {
                    main: 'Receive interview requests from employers you have selected and others that fit your interests'
                },
                {
                    main: 'Get hired!'
                }
            ]
        }
    },
}
</script>