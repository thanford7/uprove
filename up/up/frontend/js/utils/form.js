
class FormChecker {
    EMAIL_REGEX = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    WEB_LINK_REGEX = /(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/gi
    isGoodEmail(rawVal) {
        return this.EMAIL_REGEX.test(String(rawVal).toLowerCase());
    }

    isGoodWebLink(rawVal) {
        return this.WEB_LINK_REGEX.test(String(rawVal))
    }
}

export default new FormChecker();