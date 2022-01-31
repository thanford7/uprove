import dataUtil from "../../utils/data";

class SkillPrioritySelectize {
    OPTIONS = {
        REQUIRED: 'Required',
        RECOMMENDED: 'Recommended',
        OPTIONAL: 'Optional',
    }

    DEFAULT_LABEL = this.OPTIONS.RECOMMENDED

    cfg = {
        maxItems: 1,
        valueField: 'text',
        labelField: 'text',
        options: [
            {text: this.OPTIONS.REQUIRED},
            {text: this.OPTIONS.RECOMMENDED},
            {text: this.OPTIONS.OPTIONAL},
        ]
    }

    getDefault() {
        return {isRequired: 0, isRecommended: 1};
    }

    getPriorityLabel(skill) {
        const {isRequired, isRecommended} = skill;
        const skillPriorityOptions = skillPrioritySelectize.OPTIONS;
        if (dataUtil.isNil(isRequired) || dataUtil.isNil(isRequired)) {
            return skillPriorityOptions.RECOMMENDED;
        } else {
            return (isRequired) ?
                skillPriorityOptions.REQUIRED :
                ((isRecommended) ? skillPriorityOptions.RECOMMENDED : skillPriorityOptions.OPTIONAL);
        }
    }

    getPriorityValues(val) {
        if (val === this.OPTIONS.REQUIRED) {
            return {isRequired: 1, isRecommended: 0};
        } else if (val === this.OPTIONS.RECOMMENDED) {
            return this.getDefault();
        } else {
            return {isRequired: 0, isRecommended: 0};
        }
    }

    setSkillPriority(val, formData) {
        Object.assign(formData, this.getPriorityValues(val));
    }
}

const skillPrioritySelectize = new SkillPrioritySelectize();

export default skillPrioritySelectize;