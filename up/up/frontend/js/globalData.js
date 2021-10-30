const globalData = Object.assign({
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
        1: 'Novice',
        2: 'Intermediate',
        3: 'Advanced',
        4: 'Expert'
    },
    TAG_TYPE: [
        'interest',
        'skill'
    ],
    SUPPORTED_FUNCTIONS: {
        'business_analysis': 'Business analysis & consulting',
        'data_analysis': 'Data analysis',
        'product_management': 'Product managemement',
        'project_management': 'Project management',
        'customer_success': 'Customer success',
        'operations_management': 'Operations management',
        'supply_chain_management': 'Supply chain management',
        'user_experience': 'User experience',
        'marketing': 'Marketing',
        'seo': 'Search engine optimization',
        'finance': 'Finance',
        'accounting': 'Accounting',
    },
    SUPPORTED_SKILLS: {
        'excel': 'Excel',
        'powerpoint': 'PowerPoint',
        'sql': 'SQL',
        'python': 'Python',
        'bi_software': 'Business intelligence software',
        'wireframe': 'Wireframes',
    }
}, window.initData);

export default globalData;