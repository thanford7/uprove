import globalData from "../../globalData";

class CoursesSelectize {
    getCoursesCfg({isMulti = false} = {}) {
        const cfg = {
            valueField: 'id',
            labelField: 'title',
            sortField: 'title',
            searchField: 'title',
            loadThrottle: 200,
            preload: true,
            placeholder: 'Start typing to search courses'
        };
        cfg.load = (query, callback) => {
            let url = `${globalData.API_URL}course/?search=${encodeURIComponent(query)}`;
            $.ajax({
                url,
                type: 'GET',
                error: function () {
                    callback();
                },
                success: function (courses) {
                    callback(courses);
                },
            });
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

const coursesSelectize = new CoursesSelectize();

export default coursesSelectize;