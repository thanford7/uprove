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
    shorthandDateFormat = 'MMM YYYY';

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
     * Update query params and optionally redirect to a new page
     * @param params {Array}: Array of dicts with key: val pairs. The key represents the name of the query param and
     * val represents the value. Val can be a single value or a list of values
     * @param path {null|string}: Optional path if directing to a new page
     */
    setQueryParams(params, path = null) {
        if ('URLSearchParams' in window) {
            const searchParams = new URLSearchParams(window.location.search);
            params.forEach(({key, val}) => {
                searchParams.delete(key);  // Remove existing
                const vals = (Array.isArray(val)) ? val : [val];
                vals.forEach((v) => {
                    searchParams.append(key, v);
                });  // Add new values
            });
            const targetPath = path || window.location.pathname;
            const newRelativePathQuery = targetPath + '?' + searchParams.toString();
            if (path) {
                window.location.href = newRelativePathQuery;  // Redirect to new page
            } else {
                history.pushState(null, '', newRelativePathQuery); // Add to view state
            }
        }
    }

    signUpWithContext(initData) {
        this.setQueryParams([
            {key: 'next', val: window.location.pathname},
            {key: 'inviteEmployerId', val: (initData) ? this.get(initData, 'employer.id') : null}
        ], '/sign-up/');
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

    capitalize(string) {
        return (string) ? string.charAt(0).toUpperCase() + string.slice(1) : '';
    }

    /**
     * Delete an item from an object using a relative path string
     * @param obj {Object}
     * @param path {String}: Use dot notation for nested variables
     */
    deleteFromPath(obj, path) {
        path = path.split('.');

        for (let i = 0; i < path.length - 1; i++) {
            obj = obj[path[i]];
            if (typeof obj === 'undefined') {
                return;
            }
        }

        delete obj[path.pop()];
    }

    deepCopy(val) {
        return clone(val);
    }

    get(obj, path, defaultValue = undefined) {
        const keyPath = path.split('.');
        let currentTarget = obj;
        for (let i = 0; i < keyPath.length; i++) {
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

    isArraysEqual(a, b) {
        if (a === b) return true;
        if (a === null || b === null) return false;
        if (!Array.isArray(a) || !Array.isArray(b)) return false;
        if (a.length !== b.length) return false;

        // Copy before sorting so other elements aren't effected
        a = [...a];
        b = [...b];
        a.sort();
        a.sort();

        for (let i = 0; i < a.length; ++i) {
            if (a[i] !== b[i]) return false;
        }
        return true;
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

    /**
     * Returns a copied object with omitted properties removed. Does not mutate original object.
     * @param targetObject {Object}
     * @param omitList {Array}: Items in list can have relative paths using dot notation
     * @returns {*}
     */
    omit(targetObject, omitList) {
        const objCopy = this.deepCopy(targetObject);
        omitList.forEach((omission) => {
            this.deleteFromPath(objCopy, omission);
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

    sortBy(targetArray, sortKey, isInPlace = false) {
        const newArray = (isInPlace) ? targetArray : [...targetArray];
        const sortKeys = Array.isArray(sortKey) ? sortKey : [sortKey];
        sortKeys.reverse();  // Reverse the order so the first item will be sorted last (making it primary)
        sortKeys.forEach((sortKey) => {
            // Deconstruct object if sort direction has been provided
            let direction = 1;
            if (this.isObject(sortKey)) {
                direction = sortKey.direction;
                sortKey = sortKey.key;
            }
            let valGetter = (val) => this.get(val, sortKey);
            if (!this.isString(sortKey)) {
                valGetter = (val) => sortKey(val);
            }
            newArray.sort((a, b) => {
                if (valGetter(a) > valGetter(b)) {
                    return direction;
                }
                if (valGetter(b) > valGetter(a)) {
                    return -direction;
                }
                return 0;
            });
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