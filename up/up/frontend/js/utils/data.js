import dayjs from "dayjs/esm";

const NULL_DATE_STRING = '0000-00-00';  // Wordpress API returns this value if a date is null
const escapeChars = {lt: '<', gt: '>', quot: '"', apos: "'", amp: '&'};

class DataUtil {
    dateFormat = 'MM/DD/YYYY';

    parseIdString(val, separator = ',') {
        if (typeof val !== 'string') {
            return [val];
        }
        return val.split(separator);
    }

    unescapeHTML(str) {
        return str.replace(/\&([^;]+);/g, (entity, entityCode) => {
            let match;

            if (entityCode in escapeChars) {
                return escapeChars[entityCode];
            } else if (match = entityCode.match(/^#x([\da-fA-F]+)$/)) {
                return String.fromCharCode(parseInt(match[1], 16));
            } else if (match = entityCode.match(/^#(\d+)$/)) {
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
        return ((this.isNil(dateVal) || dateVal === NULL_DATE_STRING) && !isConvertNull) ? null : dayjs(dateVal);
    }

    getFileNameFromUrl(fileUrl) {
        const [fileName] = fileUrl.split('/').slice(-1);
        return fileName;
    }

    getFileType(fileName) {
        if (!fileName) {
            return null;
        }
        const [fileType] = fileName.split('.').slice(-1);
        return fileType;
    }

    getSkillLevelNumbersFromBits(skillLevelBits, allSkillLevels) {
        return Object.keys(allSkillLevels).filter((level) => parseInt(level) & skillLevelBits);
    }

    getSkillLevelsFromBits(skillLevelBits, allSkillLevels) {
        return Object.entries(allSkillLevels).reduce((levels, [level, levelName]) => {
            if (parseInt(level) & skillLevelBits) {
                levels.push(levelName);
            }
            return levels;
        }, []);
    }

    capitalize(string) {
        return (string) ? string.charAt(0).toUpperCase() + string.slice(1).toLowerCase() : '';
    }

    get(obj, path, defaultValue = undefined) {
        const travel = regexp =>
            String.prototype.split
                .call(path, regexp)
                .filter(Boolean)
                .reduce((res, key) => (res !== null && res !== undefined ? res[key] : res), obj);
        const result = travel(/[,[\]]+?/) || travel(/[,[\].]+?/);
        return result === undefined || result === obj ? defaultValue : result;
    }

    isEmpty(obj) {
        return [Object, Array].includes((obj || {}).constructor) && !Object.entries((obj || {})).length;
    }

    isNil(val) {
        return val === undefined || val === null;
    }

    isString(val) {
        return !this.isNil(val) && typeof val.valueOf() === 'string';
    }

    removeItemFromList(targetList, itemFindFn) {
        const listIdx = targetList.findIndex(itemFindFn);
        if (listIdx !== -1) {
            delete targetList[listIdx];
        }
    }

    omit(targetObject, omitList) {
        const objCopy = {...targetObject};
        omitList.forEach((omission) => {
            delete objCopy[omission];
        })
        return objCopy;
    }

    sortBy(targetArray, sortKey) {
        const newArray = [...targetArray];
        newArray.sort((a, b) => (a[sortKey] > b[sortKey]) ? 1 : ((b[sortKey] > a[sortKey]) ? -1 : 0));
        return newArray;
    }

    sum(vals) {
        if (!Array.isArray(vals)) {
            return vals;
        }
        return vals.reduce((total, val) => {
            total += val;
            return total;
        }, 0)
    }

    uniqWith(targetList, uniqFn) {
        return targetList.filter((el, idx) => targetList.findIndex((step) => uniqFn(el, step)) === idx);
    }

    uniqBy(targetList, uniqKey) {
        return this.uniqWith(targetList, (a, b) => this.get(a, uniqKey) === this.get(b, uniqKey));
    }
}

const dataUtil = new DataUtil();

export default dataUtil;