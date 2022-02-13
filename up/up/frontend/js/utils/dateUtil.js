import dayjs from "dayjs/esm";
import relativeTime from 'dayjs/plugin/relativeTime';
dayjs.extend(relativeTime);

class DateUtil {
    dateFormat = 'YYYY-MM-DD';
    timeFormat = 'H:mm:ss';

    now() {
        return dayjs();
    }

    serializeDateTime(val) {
        return dayjs(val).format(`${this.dateFormat} ${this.timeFormat}`);
    }
}
const dateUtil = new DateUtil();

export default dateUtil;