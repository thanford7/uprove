import {Popover} from "bootstrap";
import {TOOLTIPS} from "./definitions";
import {createStore, mapGetters, mapState} from "vuex";
import dataUtil from './utils/data'
import globalData, {USER_BITS} from './globalData';
import mitt from "mitt";  // https://github.com/developit/mitt
import Modal from "bootstrap/js/dist/modal";
import pluralize from 'pluralize';


const severity = {
    SUCCESS: 'success',
    WARN: 'warn',
    DANGER: 'danger'
}
let newElUid = 0;
const eventBus = mitt();

const isMobileFn = () => {
    return window.innerWidth < 768;  // md breakpoint for bootstrap
}

const store = createStore({
    state() {
        return {
            eventBus,
            isMobile: isMobileFn(),
            TOOLTIPS,
            alerts: [],
            alertCount: 0,
        }
    },
    mutations: {
        updateIsMobile(state) {
            state.isMobile = isMobileFn()
        },
        addAlert(state, alert) {
            state.alertCount++;
            state.alerts.push({...alert, id: state.alertCount});
            setTimeout(() => {
                this.commit('clearSuccessAlerts');
            }, 5000);
        },
        clearAlert(state, alertId) {
            state.alerts = state.alerts.filter((alert) => alert.id !== alertId);
        },
        clearAllAlerts(state) {
            state.alerts = [];
        },
        clearSuccessAlerts(state) {
            state.alerts = state.alerts.filter((alert) => alert.alertType !== severity.SUCCESS);
        }
    }
});

$(window).on('resize', () => {
    store.commit('updateIsMobile');
});


const ajaxRequestMixin = {
    data() {
        return {
            apiUrl: '/api/v1/',
            crudUrl: null,
            initDataKey: null,  // The key to access the data structure to be updated after CRUD operation
            isUpdateData: false,  // If true, initData will be updated on successful CRUD operation
            formData: {},  // Use for modals
            requiredFields: {}, // <formData field name>: <form DOM id>
            isAjaxModal: false,
            deleteRedirectUrl: null,  // (Optional) URL to redirect to if an entity is deleted
            pageRedirect: null  // Page to redirect to after succesful ajax request
        }
    },
    methods: {
        onSaveSuccessFn(method) {
            return (data, textStatus, xhr) => {
                eventBus.emit('ajaxSuccess', data);
                store.commit('addAlert', {
                    message: this.getSuccessMessage(data),
                    alertType: severity.SUCCESS
                });
                if (this.isUpdateData) {
                    if (method === 'DELETE') {
                        this.updateInitDataDelete(data)
                    } else {
                        this.updateInitData(data, method === 'PUT');
                    }
                }
                this.formData = {};
                if (this.isAjaxModal) {
                    this.modal$.hide();
                }

                const redirect = data.pageRedirect || this.pageRedirect;
                if (redirect) {
                    window.location.replace(redirect);
                }
            }
        },
        getSuccessMessage(data) {
            // subclass
            return 'Success';
        },
        getUpdateObject(dataKey) {
            return (dataKey) ? dataUtil.get(this.initData, dataKey) : this.initData;
        },
        updateInitData(newData, isPut) {
            if (!Array.isArray(this.initDataKey)) {
                this.initDataKey = [this.initDataKey]
            }
            this.initDataKey.forEach((dataKey) => {
                const updateObject = this.getUpdateObject(dataKey);  // Object in memory to be updated
                // Response data contains more than one data object to be mapped to in memory data
                if (dataUtil.isObject(newData) && dataKey in newData) {
                    this.initData[dataKey] = newData[dataKey];
                } else if (Array.isArray(updateObject)) {
                    if (isPut) {
                        const item = updateObject.find((item) => item.id === newData.id);
                        Object.assign(item, newData);
                    } else {
                        updateObject.push(newData);
                    }
                } else {
                    this.initData = newData;
                }
            });
        },
        updateInitDataDelete(deleteId) {
            if (this.deleteRedirectUrl) {
                window.location.replace(this.deleteRedirectUrl);
            }
            if (!deleteId) {
                return;
            }
            const updateList = this.getUpdateObject();
            dataUtil.removeItemFromList(updateList, (item) => item.id === deleteId);
        },
        onSaveFailure(xhr, textStatus, errorThrown) {
            store.commit('addAlert', {
                message: this.getFailureMessage(errorThrown, xhr),
                alertType: severity.DANGER
            });
            eventBus.emit('ajaxFailure', {xhr, textStatus, errorThrown});
        },
        getFailureMessage(errorThrown, xhr) {
            // subclass
            const responseText = xhr.responseText;
            return `${errorThrown}${(responseText) ? `: ${responseText}` : ''}`;
        },
        readForm() {
            return this.formData;
        },
        processFormData() {
            return this.readForm();
        },
        isGoodFormData(formData) {
            return this.hasRequiredFormFields(formData) & this.isGoodFormFields(formData);
        },
        isGoodFormFields(formData) {
            // subclass - add logic checks other than required fields
            return true;
        },
        hasRequiredFormFields(formData) {
            return Object.entries(this.requiredFields).reduce((hasRequired, [field, domSel]) => {
                if (!formData[field]) {
                    this.addPopover($(domSel),
                        {severity: severity.WARN, content: 'Required field', isOnce: true}
                    );
                    return false;
                }
                return hasRequired & true
            }, true);
        },
        readAndSubmitForm() {
            const formData = this.processFormData();
            if (!this.isGoodFormData(formData)) {
                return false;
            }
            return this.submitAjaxRequest(
                this.getAjaxFormData(formData, this.mediaFields),
                {method: (formData.id) ? 'PUT' : 'POST'}
            )
        },
        getAjaxFormData(data, mediaFields) {
            const ajaxData = new FormData();
            ajaxData.append('data', JSON.stringify(dataUtil.omit(data, mediaFields || [])));
            (mediaFields || []).forEach((field) => {
                if (Array.isArray(data[field])) {
                    data[field].forEach((file) => {
                        ajaxData.append(field, file);
                    })
                } else {
                    ajaxData.append(field, data[field]);
                }
            });
            return ajaxData;
        },
        saveChange(e, allowDefault = false) {
            if (!allowDefault) {
                e.preventDefault();
            }
            this.isAjaxModal = Boolean($(e.currentTarget).parents('.modal').length);
            return this.readAndSubmitForm();
        },
        deleteObject(e) {
            this.isAjaxModal = Boolean($(e.currentTarget).parents('.modal').length);
            const deleteData = this.getDeleteObjectData();
            if (!deleteData) {
                eventBus.emit('failure:delete', 'No selection');
                return;
            }
            const ajaxData = new FormData();
            ajaxData.append('data', JSON.stringify(deleteData));
            return this.submitAjaxRequest(ajaxData, {method: 'DELETE'});
        },
        getDeleteObjectData() {
            // subclass
            const formData = this.readForm();
            if (!formData.id) {
                return;
            }
            return {id: formData.id};
        },
        getAjaxCfgOverride() {
            return {};
        },
        getDeleteConfirmationMessage() {
            // subclass
            return 'Are you sure you want to delete this item?';
        },
        submitAjaxRequest(requestData, requestCfg = {}) {
            const overrides = Object.assign(this.getAjaxCfgOverride(), requestCfg);
            const method = overrides.method || 'PUT';
            if (method === 'DELETE' && this.getDeleteConfirmationMessage()) {
                if (!window.confirm(this.getDeleteConfirmationMessage())) {
                    return;
                }
            }
            return $.ajax(Object.assign({
                url: this.apiUrl + this.crudUrl,
                method,
                mode: 'same-origin',
                headers: {'X-CSRFTOKEN': $('[name=csrfmiddlewaretoken]').val()},
                data: requestData,
                contentType: false,
                processData: false,
                success: this.onSaveSuccessFn(method),
                error: this.onSaveFailure
            }, overrides));
        }
    }
}


const globalVarsMixin = {
    data() {
        return {
            globalData,
            initData: window.initData,
            djangoData: window.djangoData
        }
    },
    methods: {
        getNewElUid() {
            newElUid++;
            return newElUid.toString();
        },
        pluralize(word, count) {
            return pluralize(word, count, true);
        }
    },
    computed: {
        ...mapState({
            eventBus: 'eventBus',
            isMobile: 'isMobile',
            TOOLTIPS: 'TOOLTIPS'
        }),
        isLoggedIn() {
            return Boolean(globalData.uproveUser);
        },
        isSuperUser() {
            if (!globalData.uproveUser) {
                return false;
            }
            return globalData.uproveUser.isSuperUser;
        },
        isEmployer() {
            if (!globalData.uproveUser) {
                return false;
            }
            return Boolean(globalData.uproveUser.userTypeBits & USER_BITS.EMPLOYER);
        },
        isCandidate() {
            if (!globalData.uproveUser) {
                return false;
            }
            return Boolean(globalData.uproveUser.userTypeBits & USER_BITS.CANDIDATE);
        }
    }
}

const modalsMixin = {
    data() {
        return {
            modalName: null,
            modal$: null
        }
    },
    methods: {
        clearSelectizeElements() {
            Object.values(this.$refs).forEach((ref) => {
                if (ref && ref.elSel) {
                    ref.elSel.clear(true);
                }
            });
        },
        processRawData(rawData) {
            // subclass
            return rawData;
        },
        setEmptyFormData() {
            // subclass
            this.formData = {};
        },
        setFormFields() {
            // subclass - use for form fields that don't have a v-model property (mainly selectize fields)
        }
    },
    mounted() {
        eventBus.on(`open:${this.modalName}`, (rawData) => {
            if (!this.modal$) {
                this.modal$ = new Modal($(`#${this.modalName}`), {backdrop: 'static'});
            }
            const rawDataCopy = (rawData) ? dataUtil.deepCopy(rawData) : rawData;  // Copy data so we don't mutate original
            this.setEmptyFormData();
            this.clearSelectizeElements();
            this.modal$.show();
            if (rawDataCopy) {
                this.formData = this.processRawData(rawDataCopy);
                this.setFormFields();
            }
        });
    }
}


const popoverMixin = {
    methods: {
        addPopover(el$, {content, severity, isOnce = false}) {
            let container = 'body';
            const modal = el$.parents('.modal');
            if (modal.length) {
                container = `#${$(modal[0]).attr('id')}`;
            }
            const template = `<div class="popover ${severity}" role="tooltip"><div class="popover-arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>`
            const popover = new Popover(el$, {
                container,
                content,
                template,
                placement: 'auto'
            });
            $(container).animate({
                scrollTop: el$.offset().top
            }, 500);
            el$.focus();
            popover.show();
            if (isOnce) {
                setTimeout(() => {
                    $(container).one('click', () => {
                        popover.dispose();
                    });
                }, 1);
            }
        }
    }
}

export {ajaxRequestMixin, globalVarsMixin, modalsMixin, popoverMixin, store, severity};