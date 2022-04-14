import {addErrorAlert, getAjaxFormData, getNewElUid, makeAjaxRequest, store} from "../vueMixins";
import globalData, {SEVERITY} from "../globalData";
import dataUtil from "./data";


class LeverIntegration {
    TYPES = {
        stageChange: 'stage-change',
        archive: 'archive',
        hire: 'hire',
        delete: 'delete'
    }

    getWebhookUrl(type, employerId) {
        return `${globalData.BASE_URL}${globalData.API_URL}lever/change/${type}/${employerId}/`;
    }

    login() {
        window.location.replace(encodeURI(globalData.LEVER_REDIRECT_URL));
    }

    logout(successHook) {
        makeAjaxRequest(globalData.API_URL + 'lever/logout/', {
            method: 'POST',
            success: () => {
                store.commit('addAlert', {
                    message: 'Success: Lever integration deactivated',
                    alertType: SEVERITY.SUCCESS
                });
                if (successHook) {
                    successHook();
                }
            },
            error: addErrorAlert
        });
    }

    loadJobPostings() {
        makeAjaxRequest(globalData.API_URL + 'lever/postings/', {
            method: 'POST',
            success: () => {
                window.location.reload();
            },
            error: addErrorAlert
        })
    }

    saveToken(target$, employerId, modelName, modelValue) {
        const msgTarget = $(target$.parent().find('span')[0]);
        const tokenFn = () => {
            makeAjaxRequest(globalData.API_URL + `lever/config/${employerId}/`, {
                method: 'PUT',
                data: getAjaxFormData({[modelName]: modelValue}),
                success: () => {
                    const msgId = getNewElUid();
                    msgTarget.append(`<span id="${msgId}">&nbsp;<span class="badge -color-green -color-white-text -sub-text">Updated</span></span>`);
                    setTimeout(() => {
                        $(`#${msgId}`).remove()
                    }, 3000);
                },
                error: addErrorAlert
            });
        };
        dataUtil.debounce(tokenFn, 300)();
    }
}

const leverIntegration = new LeverIntegration();

export default leverIntegration;