import dataUtil from "../../utils/data";
import skillLevels from "./skillLevels";

class SkillSelectize {
    getSkillCfg(skills, {isMulti = true, projectId = null, isIncludeDetails = false} = {}) {
        skillLevels.setSkillLevels(skills);
        const options = dataUtil.sortBy(
            skills
                .filter((s) => projectId === s.projectId && !s.isRequired)  // Filter out required skills. Those are automatically saved
                .map((s) => ({value: s.id, text: s.name, skillLevels: s.skillLevels})),
            'text'
        );
        const cfg = {options};
        if (isIncludeDetails) {
            cfg.render = {
                option: (data, escape) => {
                    const skillLevelTxt = (data.skillLevels.length) ? data.skillLevels.join(', ') : 'All skill levels';
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