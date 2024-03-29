import globalData, {PROJECT_EVAL_CUTOFFS} from '../globalData';
import pluralize from 'pluralize';
import {eventBus, getAjaxFormData, makeAjaxRequest} from "../vueMixins";
import dateUtil from "./dateUtil";
import dayjs from "dayjs/esm";

class UserProjectUtil {

    getBadgeColor({evalCriteria=null, score=null}) {
        if (!evalCriteria && !score) {
            return 'secondary';
        }
        score = score || this.getEvaluationScore(evalCriteria);
        for (let i = 0; i < PROJECT_EVAL_CUTOFFS.length; i++) {
            const {color, cutoff} = PROJECT_EVAL_CUTOFFS[i];
            if (score <= cutoff) {
                return color;
            }
        }
        return 'secondary';
    }

    getBadgeTextColor({evalCriteria=null, score=null}) {
        if (!evalCriteria && !score) {
            return 'white';
        }
        score = score || this.getEvaluationScore(evalCriteria);
        for (let i = 0; i < PROJECT_EVAL_CUTOFFS.length; i++) {
            const {color, cutoff} = PROJECT_EVAL_CUTOFFS[i];
            if (score < cutoff) {
                return (color === 'warning') ? 'black' : 'white';
            }
        }
        return 'white';
    }

    getEvaluationScore(evalCriteria) {
        const score = evalCriteria.reduce((total, criterion) => {
            total += criterion.value || 0;
            return total;
        }, 0);
        const bestScore = evalCriteria.length * 3;
        return Math.ceil((score / bestScore) * 100);
    }

    getEvalPopoverHtml() {
        return `
            <p><b>Evaluation score</b></p>
            <p>Calculated using the following methodology:</p>
            <ul>
                <li>Each project evaluation criteria is rated on a 0-3 scale</li>
                <li>The project score is divided by the best total score (3 multiplied by the number of criteria)</li>
                <li>If multiple individuals evaluated the project, the average of all scores is used</li>
            </ul>
        `
    }

    getProjectCompleteLockedNote(userProject) {
        return 'You must upload at least one file before marking the project as complete.'
    }

    approveApplication(application, applications) {
        const ajaxData = getAjaxFormData({
            id: application.id,
            approveDateTime: dateUtil.serializeDateTime(dayjs())
        }, []);
        makeAjaxRequest(
            globalData.API_URL + 'user-job-application/',
            {
                data: ajaxData,
                method: 'PUT',
                success: (data) => {
                    const updateApp = applications.find((app) => app.id === application.id);
                    updateApp.approveDateTime = data.approveDateTime;
                    updateApp.declineDateTime = null;
                    eventBus.emit('open:celebrationModal', {msg: 'Congratulations on finding a great candidate!'});
                }
            }
        );
    }

    declineApplication(application, applications) {
        const ajaxData = getAjaxFormData({
            id: application.id,
            declineDateTime: dateUtil.serializeDateTime(dayjs())
        }, []);
        makeAjaxRequest(globalData.API_URL + 'user-job-application/',
            {
                data: ajaxData,
                method: 'PUT',
                success: (data) => {
                    const updateApp = applications.find((app) => app.id === application.id);
                    updateApp.approveDateTime = null;
                    updateApp.declineDateTime = data.declineDateTime;
                }
            }
        );
    }
}

const userProjectUtil = new UserProjectUtil();

export default userProjectUtil;