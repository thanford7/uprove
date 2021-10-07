const mainData = Object.assign({
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
        1: 'Novice',
        2: 'Intermediate',
        3: 'Advanced',
        4: 'Expert'
    },
    TAG_TYPE: [
        'interest',
        'skill'
    ]
}, window.initData);

export default mainData;