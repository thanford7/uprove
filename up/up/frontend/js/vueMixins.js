import {Popover} from "bootstrap";
import {createStore, mapState} from "vuex";
import globalData from './globalData';
import mitt from "mitt";  // https://github.com/developit/mitt
import Modal from "bootstrap/js/dist/modal";
import $ from 'jquery';


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
        onSaveSuccess() {
            // subclass
            eventBus.emit('ajaxSuccess');
            this.formData = {};
            if (this.isAjaxModal) {
                this.modal$.hide();
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
            return Object.entries(this.requiredFields).reduce((hasRequired, [field, domId]) => {
                if (!formData[field]) {
                    this.addPopover($(`#${domId}`), {content: 'Required field', isOnce: true});
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
            return this.submitAjaxRequest(formData)
        },
        saveChange(e) {
            e.preventDefault();
            this.isAjaxModal = Boolean($(e.currentTarget).parents('.modal').length)
            return this.readAndSubmitForm();
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
        }
    },
    mounted() {
        eventBus.on(`open:${this.modalName}`, () => {
            if (!this.modal$) {
                this.modal$ = new Modal($(`#${this.modalName}`));
            }
            this.clearFormData();
            this.modal$.show();
        });
    }
}


const popoverMixin = {
    methods: {
        addPopover(el$, {content, isOnce = false}) {
            let container = 'body';
            const modal = el$.parents('.modal');
            if (modal.length) {
                container = `#${$(modal[0]).attr('id')}`;
            }
            const popover = new Popover(el$, {
                container,
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

export {ajaxRequestMixin, globalVarsMixin, modalsMixin, popoverMixin, store};