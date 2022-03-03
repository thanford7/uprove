import dataUtil from "../../utils/data";
import skillLevels from "./skillLevels";

class SkillSelectize {
    getSkillCfg(skills, {isMulti = true, projectId = null, isIncludeDetails = false, isShowRequired=false, placeholder=null} = {}) {
        const cfg = {options: this.getSkillOptions(skills, projectId, isShowRequired)};
        if (placeholder) {
            cfg.placeholder = placeholder;
        }
        if (isIncludeDetails) {
            cfg.render = {
                option: (data, escape) => {
                    const skillLevelTxt = (data.skillLevels.length) ? data.skillLevels.map((sl) => sl.title).join(', ') : 'All skill levels';
                    return `
                        <div class="option" data-selectable data-value="${data.value}" style="cursor: pointer;">
                            ${escape(data.text)} (${skillLevelTxt})
                        </div>
                    `;
                }
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

    getSkillOptions(skills, projectId=null, isShowRequired=false) {
        skills = dataUtil.deepCopy(skills);  // Avoid recursive mutations
        skillLevels.setSkillLevels(skills);
        return dataUtil.sortBy(
            skills
                .filter((s) => projectId === s.projectId && (!s.isRequired || isShowRequired))  // Filter out required skills. Those are automatically saved
                .map((s) => ({value: s.id, text: s.name, skillLevels: s.skillLevels})),
            'text'
        );
    }

    getDefaultSkills(skills) {
        return skills.reduce((skillIds, skill) => {
                if (skill.isRecommended) {
                    skillIds.push(skill.id);
                }
                return skillIds;
            }, []);
    }
}

const skillSelectize = new SkillSelectize();

export default skillSelectize;