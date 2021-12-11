import Selectize from 'selectize/dist/js/standalone/selectize';

const initSelectize = () => {
    Selectize.define('uprove', function (options) {
        const self = this;

        this.setup = (function () {
            const original = self.setup;
            return function () {
                original.apply(this, arguments);

                // Open an anchor tag link from a selectize option
                this.$dropdown.on('mousedown click', '[data-selectable] a', function (e) {
                    const href = $(e.currentTarget).prop('href');
                    window.open(href, '_blank').focus();
                    e.preventDefault();
                    e.stopPropagation();
                });
            };
        })();
    });
}

export default initSelectize;