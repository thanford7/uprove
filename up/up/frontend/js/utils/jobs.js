import dataUtil from "./data";


class JobUtil {
    getLocationStr(job) {
        let location = job.location;
        if (!location) {
            location = [job.city, job.state, job.country].filter((i) => Boolean(i)).join(', ')
        }
        if (job.isRemote) {
            return `Remote: ${job.region || location || 'Anywhere'}`;
        }
        return location;
    }
}

const jobUtil = new JobUtil();

export default jobUtil;