import {Popover} from "bootstrap";
import {createStore, mapState} from "vuex";
import globalData from './globalData';
import mitt from "mitt";  // https://github.com/developit/mitt
import Modal from "bootstrap/js/dist/modal";
import $ from 'jquery';


const SEVERITY_SUCCESS = 'success';
const SEVERITY_WARN = 'warn';
const SEVERITY_DANGER = 'danger';


const eventBus = mitt();

const isMobileFn = () => {
    return window.innerWidth < 768;  // md breakpoint for bootstrap
}

const store = createStore({
    state() {
        return {
            eventBus,
            isMobile: isMobileFn()
        }
    },
    mutations: {
        updateIsMobile(state) {
            state.isMobile = isMobileFn()
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
            alerts: [],
            formData: {},
            requiredFields: {}, // <formData field name>: <form DOM id>
            isAjaxModal: false
        }
    },
    methods: {
        onSaveSuccess(data) {
            // subclass
            eventBus.emit('ajaxSuccess', data);
            this.formData = {};
            if (this.isAjaxModal) {
                this.modal$.hide();
            }
            if (data.pageRedirect) {
                window.location.replace(data.pageRedirect);
            }
        },
        onSaveFailure(xhr, textStatus, errorThrown) {
            // subclass
            eventBus.emit('ajaxFailure', {xhr, textStatus, errorThrown});
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
                        {severity: SEVERITY_WARN, content: 'Required field', isOnce: true}
                    );
                    return false;
                }
                return hasRequired & true
            }, true);
        },
        readAndSubmitForm() {
            const formData = this.processFormData();
            if(!this.isGoodFormData(formData)) {
                return false;
            }
            const ajaxData = new FormData();
            ajaxData.append('data', JSON.stringify(_.omit(formData, this.fileFields || [])));
            (this.fileFields || []).forEach((field) => { ajaxData.append(field, formData[field]); })
            return this.submitAjaxRequest(ajaxData)
        },
        saveChange(e, allowDefault=false) {
            if (allowDefault) {
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
            this.submitAjaxRequest(deleteData, {method: 'DELETE'})
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
        submitAjaxRequest(requestData, requestCfg={}) {
            return $.ajax(Object.assign({
                url: this.apiUrl + this.crudUrl,
                method: (this.formData.id) ? 'PUT': 'POST',
                mode: 'same-origin',
                headers: {'X-CSRFTOKEN': $('[name=csrfmiddlewaretoken]').val()},
                data: requestData,
                contentType: false,
                processData: false,
                success: this.onSaveSuccess,
                error: this.onSaveFailure
            }, this.getAjaxCfgOverride(), requestCfg));
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
    computed: mapState({
        eventBus: 'eventBus',
        isMobile: 'isMobile'
    })
}

const modalsMixin = {
    data() {
        return {
            modalName: null,
            modal$: null
        }
    },
    methods: {
        clearFormData() {
            // subclass for clearing selectize and other objects not directly tied to a v-model
            this.formData = {};
        },
        clearSelectizeElements() {
            Object.values(this.$refs).forEach((ref) => {
                if (ref.elSel) {
                    ref.elSel.clear(true);
                }
            });
        },
        processRawData(rawData) {
            // subclass
            return rawData;
        },
    },
    mounted() {
        eventBus.on(`open:${this.modalName}`, (rawData) => {
            if (!this.modal$) {
                this.modal$ = new Modal($(`#${this.modalName}`));
            }
            this.clearFormData();
            this.clearSelectizeElements();
            this.modal$.show();
            if (rawData) {
                this.formData = this.processRawData(rawData);
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

export {ajaxRequestMixin, globalVarsMixin, modalsMixin, popoverMixin, store};