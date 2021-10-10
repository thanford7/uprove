import dayjs from "dayjs/esm";

const NULL_DATE_STRING = '0000-00-00';  // Wordpress API returns this value if a date is null
const escapeChars = { lt: '<', gt: '>', quot: '"', apos: "'", amp: '&' };

class Data {
    dateFormat = 'MM/DD/YYYY';

    parseIdString(val, separator=',') {
        if (typeof val !== 'string') {
            return [val];
        }
        return val.split(separator);
    }

    unescapeHTML(str) {
        return str.replace(/\&([^;]+);/g, (entity, entityCode) => {
            let match;

            if ( entityCode in escapeChars) {
                return escapeChars[entityCode];
            } else if ( match = entityCode.match(/^#x([\da-fA-F]+)$/)) {
                return String.fromCharCode(parseInt(match[1], 16));
            } else if ( match = entityCode.match(/^#(\d+)$/)) {
                return String.fromCharCode(~~match[1]);
            } else {
                return entity;
            }
        });
    }

    formatDate(dateVal, {dateFormat, isReturnNull = false} = {}) {
        if (!dateVal && isReturnNull) {
            return null;
        }
        if (!dayjs.isDayjs(dateVal)) {
            dateVal = dayjs(dateVal);
        }
        if (!dateVal.isValid() && isReturnNull) {
            return null;
        }
        return dateVal.format(dateFormat || this.dateFormat);
    }

    convertToDayJS(dateVal, isConvertNull = true) {
        if (dayjs.isDayjs(dateVal)) {
            if (dateVal.isValid()) {
                return dateVal;
            }
            return (isConvertNull) ? dayjs() : null;
        }
        return ((_.isNil(dateVal) || dateVal === NULL_DATE_STRING) && !isConvertNull) ? null : dayjs(dateVal);
    }
}

export default new Data();