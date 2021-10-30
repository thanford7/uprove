import {Popover} from "bootstrap";
import {mapState} from "vuex";
import globalData from './globalData';


const ajaxRequestMixin = {
    data() {
        return {
            apiUrl: '/api/v1/',
            crudUrl: null,
            alerts: [],
            formData: {}
        }
    },
    methods: {
        onSaveSuccess() {
            this.alerts.push({
                message: 'Email sent successfully',
                alertType: 'success'
            });
        },
        onSaveFailure(xhr, textStatus, errorThrown) {
            this.alerts.push({
                message: `Email failed: ${errorThrown}`,
                alertType: 'danger'
            });
        },
        readForm() {
            return this.formData;
        },
        processFormData() {
            return this.readForm();
        },
        isGoodFormData() {
            // subclass
            return true;
        },
        readAndSubmitForm() {
            const formData = this.processFormData();
            if(!this.isGoodFormData(formData)) {
                return false;
            }
            return this.submitAjaxRequest(formData)
        },
        saveChange(e) {
            e.preventDefault();
            const isSubmitted = this.readAndSubmitForm();
            if (isSubmitted) {
                this.formData = {};
            }
        },
        getAjaxCfgOverride() {
            return {};
        },
        submitAjaxRequest(requestData) {
            return $.ajax(Object.assign({
                url: this.apiUrl + this.crudUrl,
                method: 'PUT',
                data: JSON.stringify(requestData),
                contentType: 'application/json',
                success: this.onSaveSuccess,
                error: this.onSaveFailure
            }, this.getAjaxCfgOverride()));
        }
    }
}


const globalVarsMixin = {
    data() {
        return {
            globalData
        }
    },
    computed: mapState({
        eventBus: 'eventBus',
        isMobile: 'isMobile'
    })
}


const popoverMixin = {
    methods: {
        addPopover(el$, {content, isOnce = false}) {
            const popover = new Popover(el$, {
                container: 'body',
                content,
                placement: 'auto'
            });
            el$.focus();
            popover.show();
            if(isOnce) {
                el$.one('focusout', () => {
                    popover.dispose();
                })
            }
        }
    }
}

export {ajaxRequestMixin, globalVarsMixin, popoverMixin};