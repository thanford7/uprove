import {Popover} from "bootstrap";
import layout from "./layout";


class CustomPopover {
    el$ = null;
    popover = null;

    container = 'body';
    severity = null;
    isOnce = false;
    clickTarget = null;
    onDisposeFn = null;
    showEvent = null; // {target$: <>, event: <>} example: {target$: $('#myId'), event: 'click'}

    constructor(el$, {content, severity, isOnce = false, clickTarget=null, isShow=true, onDisposeFn=null, showEvent=null}) {
        this.el$ = el$;
        this.severity = severity;
        this.isOnce = isOnce;
        this.clickTarget = clickTarget;
        this.onDisposeFn = onDisposeFn;
        this.showEvent = showEvent;
        const modal = el$.parents('.modal');
        if (modal.length) {
            this.container = `#${$(modal[0]).attr('id')}`;
        }
        this.popover = new Popover(el$, {
            container: this.container,
            content,
            template: this.getTemplate(),
            placement: 'auto'
        });
        if (isShow) {
            this.show();
        } else if (this.showEvent) {
            this.showEvent.target$.one(this.showEvent.event, this.show.bind(this));
        }
    }

    getTemplate() {
        return `<div class="popover ${this.severity}" role="tooltip"><div class="popover-arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>`
    }

    show() {
        layout.scrollTo(this.el$);
        this.el$.focus();
        this.popover.show();

        if (this.isOnce) {
            setTimeout(() => {
                $(this.clickTarget || this.container).one('click', () => {
                    this.popover.dispose();
                    if (this.onDisposeFn) {
                        this.onDisposeFn();
                    }
                });
            }, 1);
        }
    }
}

const createPopoverChain = (popoverCfgs, globalCfg = {}) => {
    popoverCfgs.reduce((lastPopover, popoverCfg, idx) => {
        const cfg = Object.assign(popoverCfg, globalCfg, {isShow: idx === 0});
        const popover = new CustomPopover(popoverCfg.el$, cfg);
        if (lastPopover && !cfg.showEvent) {
            lastPopover.onDisposeFn = () => popover.show();
        }
        return popover;
    }, null);
}

export {CustomPopover as default, createPopoverChain}