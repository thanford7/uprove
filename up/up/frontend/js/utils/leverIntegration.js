import {getFailureMessage, makeAjaxRequest, store} from "../vueMixins";
import globalData, {SEVERITY} from "../globalData";


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
            error: (xhr, textStatus, errorThrown) => {
                store.commit('addAlert', {
                    message: getFailureMessage(errorThrown, xhr),
                    alertType: SEVERITY.DANGER
                });
            }
        })
    }
}

const leverIntegration = new LeverIntegration();

export default leverIntegration;