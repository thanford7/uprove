import globalData from "../../globalData";

class TagSelectize {
    getTagCfg(tagType, {isMulti = false} = {}) {
        const cfg = {
            valueField: 'id',
            labelField: 'title',
            sortField: 'title',
            searchField: 'title',
            create: true,
            loadThrottle: 200,
            placeholder: `Start typing to see existing ${tagType}s`
        };
        cfg.load = (query, callback) => {
            if (!query.length) return callback();
            const url = `${globalData.API_URL}tag/?search=${encodeURIComponent(query)}&tagType=${encodeURIComponent(tagType)}`;
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
                        <div class="-text-bold">${escape(data.title)}</div>
                        <div class="-sub-text">${(data.description) ? escape(data.description) : ''}</div>
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

const tagSelectize = new TagSelectize();

export default tagSelectize;