const USER_BITS = {
    CANDIDATE: 1,
    EMPLOYER: 2,
    ADMIN: 4
}

const globalData = Object.assign({
    API_URL: '/api/v1/',
    ALLOWED_UPLOADS: {
        VIDEO: ['mp4', 'm4v', 'mov', 'wmv', 'avi', 'mpg'],
        IMAGE: ['png', 'jpeg', 'jpg', 'gif'],
        FILE: ['doc', 'docx', 'pdf', 'xls', 'xlsx', 'ppt', 'pptx', 'twb', 'twbx', 'pages', 'numbers', 'key', 'gdoc', 'gslides', 'gsheet']
    },
    DEGREE_OPTIONS: [
        'Associate of Arts',
        'Associate of Science',
        'Associate of Applied Science',
        'Bachelor of Arts',
        'Bachelor of Science',
        'Master of Arts',
        'Master of Science',
        'Master of Business Administration',
        'Doctoral Degree',
        'Doctor of Medicine',
        'Juris Doctor',
    ],
    EMAIL_CANDIDATE_INTEREST: 'CANDIDATE_INTEREST',
    EMAIL_CONTACT: 'CONTACT',
    EMAIL_EMPLOYER_INTEREST: 'EMPLOYER_INTEREST',
    EMPLOYMENT_OPTIONS: [
        'Full-time',
        'Part-time',
        'Self-employed',
        'Contracted',
        'Internship'
    ],
    ORGANIZATION_TYPES: [
        'company',
        'school'
    ],
    SKILL_LEVEL: {
        1: 'Entry',
        2: 'Intermediate',
        4: 'Advanced',
        8: 'Expert'
    },
    TAG_TYPE: [
        'interest',
        'skill'
    ],
    // Keep in sync with User model
    USER_TYPES: {
        [USER_BITS.CANDIDATE]: 'Candidate',
        [USER_BITS.EMPLOYER]: 'Employer',
        [USER_BITS.ADMIN]: 'Admin'
    }
}, window.globalData);

export {globalData as default, USER_BITS};