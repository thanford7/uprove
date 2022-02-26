import pluralize from 'pluralize';

class UserProjectUtil {

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