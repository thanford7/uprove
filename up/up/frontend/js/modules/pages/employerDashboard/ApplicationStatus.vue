<template>
    <div>
        <div v-if="!isUpdate">
            {{APPLICATION_STATUS[application.status]}}
            <div class="-text-small -color-moderategrey-text">
                {{getTimeDifferenceString({from: application.statusUpdateDateTime})}}&nbsp;
                <a v-if="isAllowUpdate" href="#" @click="isUpdate=true">Update</a>
            </div>
        </div>
        <div v-else>
            <ApplicationStatusSelectize
                @blur="isUpdate=false"
                @selected="setAndSave($event)"
                :excludeStatusOptions="excludeStatusOptions"/>
            <a class="-text-small" href="#" @click="isUpdate=false">Cancel</a>
        </div>
    </div>
</template>

<script>
import {APPLICATION_STATUS, APPLICATION_STATUS_KEYS} from '../../../globalData';
import ApplicationStatusSelectize from "../../inputs/ApplicationStatusSelectize";
import dataUtil from "../../../utils/data";
import dateUtil from "../../../utils/dateUtil";
import {eventBus} from "../../../vueMixins";

export default {
    name: "ApplicationStatus",
    props: ['application', 'isAllowUpdate'],
    components: {ApplicationStatusSelectize},
    data() {
        return {
            APPLICATION_STATUS,
            isUpdate: false,
            excludeStatusOptions: [
                APPLICATION_STATUS_KEYS.INVITED,
                APPLICATION_STATUS_KEYS.APPLIED,
                APPLICATION_STATUS_KEYS.WITHDRAWN
            ],
            status: null,
            isUpdateData: true
        }
    },
    methods: {
        getTimeDifferenceString: dataUtil.getTimeDifferenceString,
        getAjaxCfgOverride() {
            return {
                method: 'PUT'
            };
        },
        readForm() {
            return {
                status: this.status,
                statusUpdateDateTime: dateUtil.serializeDateTime(dateUtil.now())
            }
        },
        setAndSave(status) {
            this.status = status;
            this.saveChange();
        }
    },
    mounted() {
        this.crudUrl = `user-job-application/${this.application.id}/`;
        this.updateDataFn = (newApplication) => {
            console.log(newApplication);
            dataUtil.updateObjectInPlace(this.application, newApplication);
            if (
                [
                    APPLICATION_STATUS_KEYS.OFFER,
                    APPLICATION_STATUS_KEYS.HIRED
                ].includes(this.application.status)
            ) {
                eventBus.emit('open:celebrationModal', {msg: 'Congratulations on finding a great candidate!'});
            }
        };
    }
}
</script>