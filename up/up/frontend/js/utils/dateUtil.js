import dayjs from "dayjs/esm";
import relativeTime from 'dayjs/plugin/relativeTime';
dayjs.extend(relativeTime);

class DateUtil {
    dateFormat = 'YYYY-MM-DD';
    timeFormat = 'H:mm:ss';

    now() {
        return dayjs();
    }

    today() {
        return dayjs().hour(0).minute(0).second(0).millisecond(0);
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