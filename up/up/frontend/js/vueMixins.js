import {TOOLTIPS} from "./definitions";
import {createStore, mapState} from "vuex";
import CustomPopover, {createPopoverChain} from "./utils/popoverCustom";
import dataUtil from './utils/data'
import globalData, {SEVERITY, USER_BITS} from './globalData';
import layout from "./utils/layout";
import mitt from "mitt";  // https://github.com/developit/mitt
import Modal from "bootstrap/js/dist/modal";
import pluralize from 'pluralize';


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

            if ([SEVERITY.DANGER, SEVERITY.WARN].includes(alert.type)) {
                // If modal is open, scroll to the top, otherwise scroll to the top of the page
                const modal$ = $('.modal.show .modal-content');
                if (modal$.length) {
                    layout.scrollTo(modal$, true);
                } else {
                    layout.scrollTo($('#vue-container'));
                }
            }
        },
        clearAlert(state, alertId) {
            state.alerts = state.alerts.filter((alert) => alert.id !== alertId);
        },
        clearAllAlerts(state) {
            state.alerts = [];
        },
        clearSuccessAlerts(state) {
            state.alerts = state.alerts.filter((alert) => alert.alertType !== SEVERITY.SUCCESS);
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
            initDataKey: null,  // The key to access the data structure to be updated after CRUD operation. To update all initData, leave blank
            isUpdateData: false,  // If true, initData will be updated on successful CRUD operation
            updateDeleteMethod: null, // Set to PUT or POST if not sending a delete ID response from ajax request
            formData: {},  // Use for modals
            requiredFields: {}, // <formData field name>: <form DOM id>
            mediaFields: new Set(),  // Fields that must be processed as files or media. Can access nested fields using dot notation
            childForms: [],  // If any modals are used with "contentOnly" they must be added here so they can be cleared correctly
            isAjaxModal: false,
            deleteRedirectUrl: null,  // (Optional) URL to redirect to if an entity is deleted
            pageRedirect: null,  // Page to redirect to after succesful ajax request
            successAlertType: SEVERITY.SUCCESS,
            confirmDelete: true  // If false a window confirmation will not be required to delete
        }
    },
    methods: {
        onSaveSuccessFn(method) {
            return (data, textStatus, xhr) => {
                eventBus.emit('ajaxSuccess', data);
                store.commit('addAlert', {
                    message: this.getSuccessMessage(data, method),
                    alertType: this.successAlertType
                });
                if (this.isUpdateData) {
                    if (method === 'DELETE') {
                        if (this.updateDeleteMethod) {
                            this.updateInitData(data, this.updateDeleteMethod);
                        } else {
                            this.updateInitDataDelete(data);
                        }
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
                    window.location.href = redirect;
                }
            }
        },
        getSuccessMessage(data, method) {
            // subclass
            return 'Success';
        },
        getUpdateObject(dataKey) {
            return (dataKey) ? dataUtil.get(this.initData, dataKey) : this.initData;
        },
        updateInitData(newData, isPut) {
            if (!Array.isArray(this.initDataKey)) {
                this.initDataKey = [this.initDataKey];
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
                    Object.assign(this.initData, newData);  // This ensures Vue picks up changes (opposed to this.initData = newData)

                    // Make sure there aren't any keys that used to be present, but should be removed
                    if (dataUtil.isObject(newData) && dataUtil.isObject(this.initData)) {
                        const newKeys = Object.keys(newData);
                        Object.keys(this.initData).forEach((key) => {
                            if(!newKeys.includes(key)) {
                                delete this.initData[key];
                            }
                        });
                    }
                }
            });
            this.afterUpdateInitData();
        },
        afterUpdateInitData() {
            // subclass
        },
        updateInitDataDelete(deleteId) {
            if (this.deleteRedirectUrl) {
                window.location.replace(this.deleteRedirectUrl);
            }
            if (!deleteId) {
                return;
            }
            if (!Array.isArray(this.initDataKey)) {
                this.initDataKey = [this.initDataKey]
            }

            const updateList = this.getUpdateObject(this.initDataKey[0]);
            dataUtil.removeItemFromList(updateList, (item) => item.id === deleteId);
            this.afterDeleteInitData();

        },
        afterDeleteInitData() {
            // subclass
        },
        onSaveFailure(xhr, textStatus, errorThrown) {
            store.commit('addAlert', {
                message: this.getFailureMessage(errorThrown, xhr),
                alertType: SEVERITY.DANGER
            });
            eventBus.emit('ajaxFailure', {xhr, textStatus, errorThrown});
        },
        getFailureMessage(errorThrown, xhr) {
            // subclass
            const responseText = xhr.responseText;
            return `${this.getFailureMessagePrepend()}${errorThrown}${(responseText && !responseText.includes('<!DOCTYPE html>')) ? `: ${responseText}` : ''}`;
        },
        getFailureMessagePrepend() {
            // subclass
            return '';
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
                if (!dataUtil.get(formData, field)) {
                    this.addPopover($(domSel),
                        {severity: SEVERITY.WARN, content: 'Required field', isOnce: true}
                    );
                    return false;
                }
                return hasRequired & true
            }, true);
        },
        getAndCheckData() {
            const formData = this.processFormData();
            const isGoodData = this.isGoodFormData(formData);
            return {formData, isGoodData};
        },
        readAndSubmitForm() {
            const formData = this.processFormData();
            if (!this.isGoodFormData(formData)) {
                return false;
            }
            return this.submitAjaxRequest(
                this.getAjaxFormData(formData),
                {method: (formData.id) ? 'PUT' : 'POST'}
            )
        },
        /**
         * Transforms an object into form data. Splits media data (files, images, videos) into separate fields so they
         * can be processed differently
         * @param data {Object}
         * @returns {FormData}
         */
        getAjaxFormData(data) {
            const ajaxData = new FormData();
            ajaxData.append('data', JSON.stringify(dataUtil.omit(data, this.mediaFields)));
            this.mediaFields.forEach((field) => {
                const val = dataUtil.get(data, field);
                if (!val) {
                    return;
                }
                const finalField = field.split('.').reduce((finalField, fieldPart, idx) => {
                    if (idx !== 0) {
                        fieldPart = dataUtil.capitalize(fieldPart);
                    }
                    return finalField + fieldPart;
                }, ''); // If field uses dot notation, we need to use the last subfield
                if (Array.isArray(val)) {
                    val.forEach((file) => {
                        ajaxData.append(finalField, file);
                    })
                } else {
                    ajaxData.append(finalField, val);
                }
            });
            return ajaxData;
        },
        saveChange(e, allowDefault = false) {
            if (e && !allowDefault) {
                e.preventDefault();
            }
            this.isAjaxModal = (e) ? Boolean($(e.currentTarget).parents('.modal').length) : false;
            return this.readAndSubmitForm();
        },
        deleteObject(e) {
            this.isAjaxModal = (e) ? Boolean($(e.currentTarget).parents('.modal').length) : false;
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
            const overrides = Object.assign(requestCfg, this.getAjaxCfgOverride());
            const method = overrides.method || 'PUT';
            if (method === 'DELETE' && this.confirmDelete && this.getDeleteConfirmationMessage()) {
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
        log(val) {
            console.log(val);  // Easy way to debug Vue html code
        },
        getSkillLevelNumbersFromBits(skillLevelBits) {
            return Object.keys(this.globalData.SKILL_LEVEL).filter((level) => parseInt(level) & skillLevelBits);
        },
        getSkillLevelsFromBits(skillLevelBits) {
            return Object.entries(this.globalData.SKILL_LEVEL).reduce((levels, [levelBit, level]) => {
                if (parseInt(levelBit) & skillLevelBits) {
                    levels.push(level);
                }
                return levels;
            }, []);
        },
        redirectUrl(url, isNewTab=false) {
            if (isNewTab) {
                window.open(url, '_blank');
            } else {
                window.location.replace(url);
            }
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
            return Boolean(globalData.uproveUser && globalData.uproveUser.isAuthenticated);
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
        },
        isAdmin() {
            if (!globalData.uproveUser) {
                return false;
            }
            return Boolean(globalData.uproveUser.userTypeBits & USER_BITS.ADMIN);
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
        initForm() {
            this.formData = this.getEmptyFormData();
            eventBus.emit('formClear');  // Clear all non-reactive elements
        },
        processRawData(rawData) {
            // subclass
            return rawData;
        },
        getEmptyFormData() {
            // subclass
            return {};
        },
        setFormFields() {
            // subclass - use for form fields that don't have a v-model property (mainly selectize fields)
        },
        setFormData(rawData) {
            if (rawData) {
                const rawDataCopy = (rawData) ? dataUtil.deepCopy(rawData) : rawData;  // Copy data so we don't mutate original
                this.formData = this.processRawData(rawDataCopy);
                this.setFormFields();
            }
        }
    },
    mounted() {
        eventBus.on(`open:${this.modalName}`, (rawData) => {
            this.modal$ = Modal.getOrCreateInstance($(`#${this.modalName}`), {backdrop: 'static'});
            store.commit('clearAllAlerts');
            this.initForm();
            this.modal$.show();
            this.setFormData(rawData);
        });
        eventBus.on(`open:${this.modalName}:content`, (rawData) => {
            this.initForm();
            this.setFormData(rawData);
        });
    }
}


const popoverMixin = {
    methods: {
        addPopover(el$, popoverCfg = {}) {
            return new CustomPopover(el$, popoverCfg);
        },
        createPopoverChain
    }
}

export {ajaxRequestMixin, globalVarsMixin, modalsMixin, popoverMixin, store};