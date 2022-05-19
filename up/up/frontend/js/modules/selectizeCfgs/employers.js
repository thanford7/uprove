import globalData from "../../globalData";

class EmployersSelectize {
    getEmployersCfg({isMulti = false} = {}) {
        const cfg = {
            valueField: 'id',
            sortField: 'companyName',
            searchField: 'companyName',
            loadThrottle: 200,
            placeholder: 'Start typing to search employers'
        };
        cfg.load = (query, callback) => {
            if (!query.length) return callback();
            let url = `${globalData.API_URL}account-employer/?search=${encodeURIComponent(query)}`;
            $.ajax({
                url,
                type: 'GET',
                error: function () {
                    callback();
                },
                success: function (users) {
                    callback(users);
                },
            });
        }
        cfg.render = {
            option: (data, escape) => {
                return `
                    <div class="option" data-selectable data-value="${data.id}" style="cursor: pointer;">
                        ${escape(data.companyName)}
                    </div>
                `;
            },
            item: (data, escape) => {
                return `<div className="item" data-value="${data.id}">${escape(data.companyName)}</div>`
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

    // Pass to the selectize' load method
    loadEmployerByIdFn(employerId, selectizeComponent) {
        return function (callback) {
            let url = `${globalData.API_URL}account-employer/${employerId}/`;
            $.ajax({
                url,
                type: 'GET',
                error: function () {
                    callback();
                },
                success: function (user) {
                    // callback([user]);
                    selectizeComponent.resetOptions([user]);
                    selectizeComponent.elSel.setValue(employerId);
                },
            });
        }
    }
}

const employersSelectize = new EmployersSelectize();

export default employersSelectize;