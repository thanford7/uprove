import {PROJECT_EVAL_CUTOFFS} from '../globalData';
import pluralize from 'pluralize';

class UserProjectUtil {

    getBadgeColor({evalCriteria=null, score=null}) {
        if (!evalCriteria && !score) {
            return 'secondary';
        }
        score = score || this.getEvaluationScore(evalCriteria);
        for (let i = 0; i < PROJECT_EVAL_CUTOFFS.length; i++) {
            const {color, cutoff} = PROJECT_EVAL_CUTOFFS[i];
            if (score < cutoff) {
                return color;
            }
        }
        return 'secondary';
    }

    getEvaluationScore(evalCriteria) {
        const score = evalCriteria.reduce((total, criterion) => {
            total += criterion.value || 0;
            return total;
        }, 0);
        const bestScore = evalCriteria.length * 3;
        return Math.round((score / bestScore) * 100);
    }

    getProjectCompleteLockedNote(userProject) {
        if (!userProject.files.length) {
            return 'You must upload at least one file before marking the project as complete.'
        }
        return this.getProjectLockedNote(userProject);
    }

    getProjectLockedNote(userProject) {
        if (userProject.isLocked) {
            return `Project cannot be changed for another ${pluralize('day', userProject.daysUntilUnlock, true)} to give employers time to review`
        }
        return null;
    }
}

const userProjectUtil = new UserProjectUtil();

export default userProjectUtil;