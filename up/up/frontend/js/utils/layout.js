class Layout {
    heightErrorMarginPx = 2;

    isElHeightExceeded(el$) {
        if (el$ && el$[0]) {
            const {clientHeight, scrollHeight, clientWidth, scrollWidth} = el$[0];
            return scrollHeight > clientHeight + this.heightErrorMarginPx || scrollWidth > clientWidth + this.heightErrorMarginPx;
        }
    }

    scrollTo(el$, isTop=false) {
        let container = 'body';
        const modal = el$.parents('.modal');
        if (modal.length) {
            container = `#${$(modal[0]).attr('id')} .modal-body`;
        }
        $(container).animate({
            scrollTop: (isTop) ? 0 : el$.offset().top
        }, 500);
    }
}

const layout = new Layout();

export default layout;