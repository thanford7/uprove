import dataUtil from "./data";


class JobUtil {
    getLocationStr(job) {
        if (job.isRemote) {
            return `Remote: ${job.region || 'Anywhere'}`;
        }
        return ['city', 'state', 'country'].reduce((locationStr, locationPart) => {
            const locationPartStr = dataUtil.get(job, locationPart);
            if (!locationPartStr) {
                return locationStr;
            }
            if (locationStr === '') {
                locationStr = locationPartStr;
            } else {
                locationStr += `, ${locationPartStr}`;
            }
            return locationStr
        }, '');
    }
}

const jobUtil = new JobUtil();

export default jobUtil;