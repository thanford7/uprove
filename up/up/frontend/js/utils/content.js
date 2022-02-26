import {CONTENT_TYPES} from '../globalData';

class ContentUtil {

    getContentTitle(item) {
        if (!item) {
            return null;
        }
        if ([CONTENT_TYPES.IMAGE, CONTENT_TYPES.VIDEO, CONTENT_TYPES.CUSTOM].includes(item.type)) {
            return item.title;
        } else if (item.type === CONTENT_TYPES.EDUCATION) {
            return `${item.school.name}: ${item.degree}`;
        } else if (item.type === CONTENT_TYPES.EXPERIENCE) {
            return `${item.organization.name}: ${item.positionTitle}`;
        } else if (item.type === CONTENT_TYPES.PROJECT) {
            return `${item.customProject.role}: ${item.customProject.projectTitle}`;
        }
    }
}

const contentUtil = new ContentUtil();

export default contentUtil;