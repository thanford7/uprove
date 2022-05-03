const USER_BITS = {
    CANDIDATE: 1,
    EMPLOYER: 2,
    ADMIN: 4
}

const REMOTE_BITS = {
    NON_REMOTE: 1,
    REMOTE: 2
}

const PROJECT_EVAL_CUTOFFS = [
    {cutoff: 50, color: 'danger'},
    {cutoff: 80, color: 'warning'},
    {cutoff: 100, color: 'success'}
]

const PROFILE_SECTIONS = {
    PROJECTS: 'PROJECTS',
    EXPERIENCE: 'EXPERIENCE',
    EDUCATION: 'EDUCATION'
}

const CONTENT_TYPES = {
    EXISTING: 'existing',
    EXPERIENCE: 'experience',
    EDUCATION: 'education',
    CERTIFICATION: 'certification',
    PROJECT: 'project',
    CUSTOM: 'custom',
    VIDEO: 'video',
    IMAGE: 'image',
    FILE: 'file',
    TEXT: 'text'
}

const DEGREE_OPTIONS = [
    'Associate of Arts',
    'Associate of Science',
    'Associate of Applied Science',
    'Bachelor of Arts',
    'Bachelor of Science',
    'Certificate',
    'Master of Arts',
    'Master of Science',
    'Master of Business Administration',
    'Doctoral Degree',
    'Doctor of Medicine',
    'Juris Doctor',
]

const ORGANIZATION_TYPES = {
    COMPANY: 'company',
    SCHOOL: 'school'
};

const PROJECT_STATUSES = {
    DRAFT: 'draft',
    HIDDEN: 'hidden',
    COMPLETE: 'complete'
}

const SEVERITY = {
    SUCCESS: 'success',
    WARN: 'warn',
    DANGER: 'danger',
    INFO: 'info'
};

const TAG_TYPES = {
    INTEREST: 'interest',
    SKILL: 'skill'
}

const globalDataGetter = () => {
    return Object.assign({
        API_URL: '/api/v1/',
        ALLOWED_UPLOADS: {
            VIDEO: ['mp4', 'm4v', 'mov', 'wmv', 'avi', 'mpg'],
            IMAGE: ['png', 'jpeg', 'jpg', 'gif'],
            FILE: ['doc', 'docx', 'pdf', 'xls', 'xlsx', 'ppt', 'pptx', 'twb', 'twbx', 'pages', 'numbers', 'key', 'gdoc', 'gslides', 'gsheet']
        },
        CANDIDATE_SUPPORT_EMAIL: 'community@uprove.co',
        SEND_EMAIL: 'no_reply@uprove.co',
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
        LOOM_API_KEY: 'db47f7c0-e863-4ed8-ac6e-2c9872ad5c00',
        // Number of days that a project cannot be updated after its status is changed to "COMPLETE"
        // This prevents candidates from changing the project once it has been submitted to an employer
        PROJECT_COMPLETE_LOCK_DAYS: 30,
        PROJECT_STATUSES,
        SKILL_LEVEL: {
            1: {
                title: 'Entry',
                description: 'Comparable with 0-2 years experience',
                pct: 25
            },
            2: {
                title: 'Intermediate',
                description: 'Comparable with 3-5 years experience',
                pct: 50
            },
            4: {
                title: 'Advanced',
                description: 'Comparable with 6-8 years experience',
                pct: 75
            },
            8: {
                title: 'Expert',
                description: 'Comparable with 9+ years experience',
                pct: 100
            }
        },
        // Keep in sync with User model
        USER_TYPES: {
            [USER_BITS.CANDIDATE]: 'Candidate',
            [USER_BITS.EMPLOYER]: 'Employer',
            [USER_BITS.ADMIN]: 'Admin'
        }
    }, window.globalData)
};

const globalData = globalDataGetter();

export {globalData as default, CONTENT_TYPES, DEGREE_OPTIONS, ORGANIZATION_TYPES, PROFILE_SECTIONS, PROJECT_EVAL_CUTOFFS,
    PROJECT_STATUSES, REMOTE_BITS, SEVERITY, TAG_TYPES, USER_BITS};