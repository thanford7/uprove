import dataUtil from "../../utils/data";
import globalData from "../../globalData";

class SkillLevelSelectize {
    getSkillLevelCfg(skillLevels, isMulti=true) {
        const options = Object.entries(skillLevels).map(([key, level]) => ({value: key, text: level.title}));
        if (isMulti) {
            return {
                plugins: ['remove_button'],
                maxItems: null,
                options
            };
        }
        return {
            maxItems: 1,
            options
        };
    }

    /**
     * Sets skill levels from bits
     * @param objList {Array}: A list of objects, each of which must have a "skillLevelBits" property
     * @param isSingle {Boolean}: If true, the singular version of skillLevelBits will be used as the key
     */
    setSkillLevels(objList, isSingle = false) {
        const skillLevelBitKey = (isSingle) ? 'skillLevelBit' : 'skillLevelBits';
        objList.forEach((obj) => {
            const skillLevels = Object.entries(globalData.SKILL_LEVEL).reduce((skillLevels, [skillLevelBit, skillLevel]) => {
                if (skillLevelBit & obj[skillLevelBitKey]) {
                    skillLevels.push(skillLevel);
                }
                return skillLevels;
            }, []);

            // Check whether skill levels have already been set to avoid recursive mutations
            if (!obj.skillLevels || !dataUtil.isArraysEqual(obj.skillLevels, skillLevels)) {
                obj.skillLevels = skillLevels;
            }
        });
    }
}

const skillLevelSelectize = new SkillLevelSelectize();

export default skillLevelSelectize;