import globalData from "../../globalData";

class UsersSelectize {
    getUsersCfg({isMulti = false} = {}) {
        const cfg = {
            valueField: 'id',
            sortField: ['firstName', 'lastName'],
            searchField: ['firstName', 'lastName', 'email'],
            loadThrottle: 200,
            placeholder: 'Start typing to search users'
        };
        cfg.load = (query, callback) => {
            if (!query.length) return callback();
            let url = `${globalData.API_URL}account-user/?search=${encodeURIComponent(query)}`;
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
                        ${escape(data.firstName)} ${escape(data.lastName)} (${escape(data.email)})
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

const usersSelectize = new UsersSelectize();

export default usersSelectize;