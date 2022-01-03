import dayjs from "dayjs/esm";
import relativeTime from 'dayjs/plugin/relativeTime';
dayjs.extend(relativeTime);

class DateSerializer {
    dateFormat = 'YYYY-MM-DD';
    timeFormat = 'H:mm:ss';

    serializeDateTime(val) {
        return dayjs(val).format(`${this.dateFormat} ${this.timeFormat}`);
    }
}
const dateSerializer = new DateSerializer();

export {dateSerializer};