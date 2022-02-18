import globalData from "../../globalData";

class OrganizationSelectize {
    getOrgCfg({isMulti = false, orgType=null} = {}) {
        const cfg = {
            valueField: 'id',
            labelField: 'name',
            sortField: 'name',
            searchField: 'name',
            create: true,
            loadThrottle: 500,
            placeholder: 'Start typing to see existing orgs'
        };
        cfg.load = (query, callback) => {
            if (!query.length) return callback();
            let url = `${globalData.API_URL}/organization/?search=${encodeURIComponent(query)}`;
            if (orgType) {
                url += `&orgType=${encodeURIComponent(orgType)}`
            }
            $.ajax({
                url,
                type: 'GET',
                error: function () {
                    callback();
                },
                success: function (res) {
                    callback(res);
                },
            });
        }
        cfg.render = {
            option: (data, escape) => {
                return `
                    <div class="option" data-selectable data-value="${data.id}" style="cursor: pointer;">
                        ${escape(data.name)}
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

const orgSelectize = new OrganizationSelectize();

export default orgSelectize;