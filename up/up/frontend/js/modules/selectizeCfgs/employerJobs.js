import globalData from "../../globalData";

class EmployerJobsSelectize {
    getEmployerJobsCfg(employerId, {isMulti = false, filterFn=null} = {}) {
        const cfg = {
            valueField: 'id',
            labelField: 'jobTitle',
            sortField: 'jobTitle',
            searchField: 'jobTitle',
            loadThrottle: 500,
            placeholder: 'Start typing to search jobs'
        };
        cfg.load = (query, callback) => {
            if (!query.length) return callback();
            let url = `${globalData.API_URL}job-posting/?employerId=${employerId}&search=${encodeURIComponent(query)}`;
            $.ajax({
                url,
                type: 'GET',
                error: function () {
                    callback();
                },
                success: function (jobs) {
                    if (filterFn) {
                        jobs = filterFn(jobs);
                    }
                    callback(jobs);
                },
            });
        }
        cfg.render = {
            option: (data, escape) => {
                const locationStr = (data.location) ? `<div class="-sub-text">${escape(data.location)}</div>` : '';
                return `
                    <div class="option" data-selectable data-value="${data.id}" style="cursor: pointer;">
                        ${escape(data.jobTitle)}${locationStr}
                    </div>
                `;
            }
        }
        if (isMulti) {
            return Object.assign({
                plugins: ['remove_button'],
                maxItems: null
            }, cfg);
        }
        return Object.assign({maxItems: 1}, cfg);
    }
}

const employerJobsSelectize = new EmployerJobsSelectize();

export default employerJobsSelectize;