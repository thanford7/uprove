class Layout {
    heightErrorMarginPx = 2;

    isElHeightExceeded(el$) {
        if (el$ && el$[0]) {
            const {clientHeight, scrollHeight, clientWidth, scrollWidth} = el$[0];
            return scrollHeight > clientHeight + this.heightErrorMarginPx || scrollWidth > clientWidth + this.heightErrorMarginPx;
        }
    }
}

export default new Layout;