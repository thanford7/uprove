import globalData from "../globalData";

class CustomProjectUtil {
    getLink(customProject, isAbsolute=false) {
        if (!customProject) {
            return null;
        }
        const skillHref = (customProject.skillIds || []).reduce((skillHref, sId) => {
            skillHref += `&skill=${sId}`;
            return skillHref;
        }, '');
        return `${(isAbsolute) ? globalData.BASE_URL : ''}/project/${customProject.projectId}/?skillLevel=${customProject.skillLevelBit}${skillHref}`;
    }
}

const customProjectUtil = new CustomProjectUtil();

export default customProjectUtil;