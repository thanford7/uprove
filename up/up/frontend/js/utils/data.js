import dayjs from "dayjs/esm";
import relativeTime from 'dayjs/plugin/relativeTime';

dayjs.extend(relativeTime);

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
            return `Approved ${dayjs().to(dayjs(jobApplication.approveDateTime))}`;
        } else if (jobApplication.declineDateTime) {
            return `Declined ${dayjs().to(dayjs(jobApplication.declineDateTime))}`;
        } else if (jobApplication.submissionDateTime) {
            return `Submitted ${dayjs().to(dayjs(jobApplication.submissionDateTime))}`;
        } else if (jobApplication.withdrawDateTime) {
            return `Withdrawn ${dayjs().to(dayjs(jobApplication.withdrawDateTime))}`;
        } else {
            return 'Not submitted';
        }
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
            targetList.splice(listIdx, 1);
        }
    }

    omit(targetObject, omitList) {
        const objCopy = {...targetObject};
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