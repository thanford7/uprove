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
            obj.skillLevels = Object.entries(globalData.SKILL_LEVEL).reduce((skillLevels, [skillLevelBit, skillLevel]) => {
                if (skillLevelBit & obj[skillLevelBitKey]) {
                    skillLevels.push(skillLevel);
                }
                return skillLevels;
            }, []);
        });
    }
}

const skillLevelSelectize = new SkillLevelSelectize();

export default skillLevelSelectize;