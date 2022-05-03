<template>
    <HamburgerDropdown :elId="getNewElUid()">
        <li>
            <a class="dropdown-item" href="#"><i class="far fa-envelope"></i>
                Message</a>
        </li>
        <li
            v-if="getApplicationStatus(application) !== APPLICATION_STATUS.NOT_SUBMITTED && application.userProject"
        >
            <a class="dropdown-item" :href="`/user-project/${application.userProject.id}`" target="_blank">
                <i class="fas fa-external-link-alt"></i> View application
            </a>
        </li>
        <li @click="approveApplication(application, applications)">
            <a class="dropdown-item" href="#">
                <i class="far fa-thumbs-up -color-green-text"></i> Approve
                <InfoToolTip :elId="getNewElUid()" :content="TOOLTIPS.employerApprove"/>
            </a>
        </li>
        <li @click="declineApplication(application, applications)">
            <a class="dropdown-item" href="#">
                <i class="far fa-thumbs-down -color-red-text"></i> Decline
                <InfoToolTip :elId="getNewElUid()" :content="TOOLTIPS.employerDecline"/>
            </a>
        </li>
    </HamburgerDropdown>
</template>

<script>
import dataUtil, {APPLICATION_STATUS} from "../../../utils/data";
import HamburgerDropdown from "../../components/HamburgerDropdown";
import InfoToolTip from "../../components/InfoToolTip";
import userProjectUtil from "../../../utils/userProject";

export default {
    name: "ApplicationDropdownOpts",
    props: ['application', 'applications'],
    components: {HamburgerDropdown, InfoToolTip},
    data() {
        return {
            APPLICATION_STATUS,
        }
    },
    methods: {
        approveApplication: userProjectUtil.approveApplication,
        declineApplication: userProjectUtil.declineApplication,
        getApplicationStatus: dataUtil.getApplicationStatus,
    }
}
</script>
