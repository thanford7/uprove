import dayjs from "dayjs/esm";
import pluralize from 'pluralize';
import relativeTime from 'dayjs/plugin/relativeTime';
dayjs.extend(relativeTime);

const SECONDS_IN_MINUTE = 60;
const SECONDS_IN_HOUR = 60 * 60;
const SECONDS_IN_DAY = 60 * 60 * 24;

class DateUtil {
    dateFormat = 'YYYY-MM-DD';
    timeFormat = 'H:mm:ss';

    now() {
        return dayjs();
    }

    today() {
        return dayjs().hour(0).minute(0).second(0).millisecond(0);
    }

    getTimeRemaining(targetDt) {
        const diffSeconds = dayjs(targetDt).diff(this.now(), 's');
        if (diffSeconds <= 0) {
            return 'No time remaining';
        }
        const timeComponents = [];
        const days = Math.floor(diffSeconds / SECONDS_IN_DAY);
        if (days) {
            timeComponents.push(pluralize('day', days, true));
        }
        let remainder = diffSeconds - days * SECONDS_IN_DAY;
        const hours = Math.floor(remainder / SECONDS_IN_HOUR);
        if (hours) {
            timeComponents.push(pluralize('hour', hours, true));
        }
        remainder = remainder - hours * SECONDS_IN_HOUR;
        const minutes = Math.floor(remainder / SECONDS_IN_MINUTE);
        if (minutes) {
            timeComponents.push(pluralize('minute', minutes, true));
        }
        return timeComponents.join(' ')
    }

    serializeDate(val) {
        return dayjs(val).format(`${this.dateFormat}`);
    }

    serializeDateTime(val) {
        return dayjs(val).format(`${this.dateFormat} ${this.timeFormat}`);
    }
}
const dateUtil = new DateUtil();

export default dateUtil;