import clone from 'just-clone';
import dayjs from "dayjs/esm";
import relativeTime from 'dayjs/plugin/relativeTime';

dayjs.extend(relativeTime);

const escapeChars = {lt: '<', gt: '>', quot: '"', apos: "'", amp: '&'};
const APPLICATION_STATUS = {
    NOT_SUBMITTED: 'Not submitted',
    SUBMITTED: 'Submitted',
    APPROVED: 'Approved',
    DECLINED: 'Declined',
    WITHDRAWN: 'Withdrawn'
}

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
        return (this.isNil(dateVal) && !isConvertNull) ? null : dayjs(dateVal);
    }

    getFileNameFromUrl(fileUrl) {
        const [fileName] = fileUrl.split('/').slice(-1);
        return fileName;
    }

    getQueryParams() {
        const searchParams = new URLSearchParams(window.location.search);
        const paramDict = {};
        for (const [key, val] of searchParams.entries()) {
            if (key in paramDict) {
                const currentVal = paramDict[key];
                if (Array.isArray(currentVal)) {
                    currentVal.push(val);
                } else {
                    paramDict[key] = [currentVal, val];
                }
            } else {
                paramDict[key] = val;
            }
        }
        return paramDict;
    }

    /**
     * We can't add meta data directly onto file objects and order is not guaranteed when pairing files with
     * their respective meta data. To handle this, file objects and file meta data are processed into a dictionary
     * where the lookup value is based on the file object's name. This is the only "unique" key that the file object
     * possesses. It is possible for a file object to have the same name as another, so duplicate file names should
     * be guarded against when testing for good form data
     * @param files {Object|Array} Values are objects which contain meta data and a file
     * @param metaDataKey {string} The dictionary key which all meta data is assigned to
     * @param dataKey {string} The dictionary key which all file objects are assigned
     * @param fileKey {string} The dictionary key to get the file from each respective file object
     * @returns {Object}
     */
    getFileFormatForAjaxRequest(files, metaDataKey, dataKey, fileKey) {
        if (!Array.isArray(files)) {
            files = Object.values(files);
        }
        files = files.filter((file) => !this.isNil(file[fileKey]));
        return {
            [metaDataKey]: files.map((file) => {
                return Object.assign(
                    this.omit(file, [fileKey]),
                    {fileKey: this.isString(file[fileKey]) ? null : file[fileKey].name}
                )
            }),
            [dataKey]: files.map((file) => file[fileKey])
        };
    }

    getFileType(fileName) {
        if (!fileName) {
            return null;
        }
        const [fileType] = fileName.split('.').slice(-1);
        return fileType;
    }

    getApplicationStatus(jobApplication) {
        if (jobApplication.approveDateTime) {
            return `${APPLICATION_STATUS.APPROVED} ${dayjs().to(dayjs(jobApplication.approveDateTime))}`;
        } else if (jobApplication.declineDateTime) {
            return `${APPLICATION_STATUS.DECLINED} ${dayjs().to(dayjs(jobApplication.declineDateTime))}`;
        } else if (jobApplication.submissionDateTime) {
            return `${APPLICATION_STATUS.SUBMITTED} ${dayjs().to(dayjs(jobApplication.submissionDateTime))}`;
        } else if (jobApplication.withdrawDateTime) {
            return `${APPLICATION_STATUS.WITHDRAWN} ${dayjs().to(dayjs(jobApplication.withdrawDateTime))}`;
        } else {
            return APPLICATION_STATUS.NOT_SUBMITTED;
        }
    }

    /**
     * Sets skill levels from bits
     * @param objList {Array}: A list of objects, each of which must have a "skillLevelBits" property
     * @param globalData {Object}
     * @param isSingle {Boolean}: If true, the singular version of skillLevelBits will be used
     */
    setSkillLevels(objList, globalData, isSingle = false) {
        const skillLevelBitKey = (isSingle) ? 'skillLevelBit' : 'skillLevelBits';
        objList.forEach((obj) => {
            obj.skillLevels = Object.entries(globalData.SKILL_LEVEL).reduce((skillLevels, [skillLevelBit, skillLevel]) => {
                if (skillLevelBit & obj[skillLevelBitKey]) {
                    skillLevels.push(skillLevel);
                }
                return skillLevels;
            }, []);
        });
    }

    capitalize(string) {
        return (string) ? string.charAt(0).toUpperCase() + string.slice(1).toLowerCase() : '';
    }

    deepCopy(val) {
        return clone(val);
    }

    get(obj, path, defaultValue = undefined) {
        const keyPath = path.split('.');
        let currentTarget = obj;
        for (let i=0; i<keyPath.length; i++) {
            currentTarget = currentTarget[keyPath[i]];
            if (!currentTarget) {
                return defaultValue;
            }
        }
        return currentTarget;
    }

    groupByKey(targetArray, key) {
        return targetArray.reduce((r, v, i, a, k = this.get(v, key)) => ((r[k] || (r[k] = [])).push(v), r), {})
    }

    groupByFn(targetArray, fn) {
        return targetArray.reduce((r, v, i, a, k = fn(v)) => ((r[k] || (r[k] = [])).push(v), r), {})
    }

    isEmpty(obj) {
        return [Object, Array].includes((obj || {}).constructor) && !Object.entries((obj || {})).length;
    }

    isObject(val) {
        return (
            typeof val === 'object' &&
            !Array.isArray(val) &&
            val !== null
        )
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
            targetList.splice(listIdx, 1);
        }
    }

    omit(targetObject, omitList) {
        const objCopy = this.deepCopy(targetObject);
        omitList.forEach((omission) => {
            delete objCopy[omission];
        })
        return objCopy;
    }

    pick(object, keys) {
        return keys.reduce((obj, key) => {
            if (object && object.hasOwnProperty(key)) {
                obj[key] = object[key];
            }
            return obj;
        }, {});
    }

    sortBy(targetArray, sortKey, isInPlace=false) {
        const newArray = (isInPlace) ? targetArray : [...targetArray];
        const sortKeys = Array.isArray(sortKey) ? sortKey : [sortKey];
        sortKeys.reverse();  // Reverse the order so the first item will be sorted last (making it primary)
        sortKeys.forEach((sortKey) => {
            newArray.sort((a, b) => (this.get(a, sortKey) > this.get(b, sortKey)) ? 1 : ((this.get(b, sortKey) > this.get(a, sortKey)) ? -1 : 0));
        });
        return newArray;
    }

    sum(vals) {
        if (!Array.isArray(vals)) {
            return vals;
        }
        return vals.reduce((total, val) => {
            if (isNaN(val)) {
                if (val.includes('.')) {
                    val = Number.parseFloat(val);
                } else {
                    val = Number.parseInt(val);
                }
            }
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

export {dataUtil as default, APPLICATION_STATUS};