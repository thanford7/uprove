
const APPLICATION_STATUS_KEYS = {
    INVITED: 'INVITED',
    APPLIED: 'APPLIED',
    APPROVED_NO_INTERVIEW: 'APPROVED_NO_INTERVIEW',
    APPROVED_INTERVIEW: 'APPROVED_INTERVIEW',
    DECLINED: 'DECLINED',
    WITHDRAWN: 'WITHDRAWN',
    OFFER: 'OFFER',
    HIRED: 'HIRED'
};

const APPLICATION_STATUS = {
    [APPLICATION_STATUS_KEYS.INVITED]: 'Invited',
    [APPLICATION_STATUS_KEYS.APPLIED]: 'Applied',
    [APPLICATION_STATUS_KEYS.APPROVED_NO_INTERVIEW]: 'Approved - Interviews not started',
    [APPLICATION_STATUS_KEYS.APPROVED_INTERVIEW]: 'Approved - Interviews started',
    [APPLICATION_STATUS_KEYS.DECLINED]: 'Declined',
    [APPLICATION_STATUS_KEYS.WITHDRAWN]: 'Withdrawn',
    [APPLICATION_STATUS_KEYS.OFFER]: 'Offer extended',
    [APPLICATION_STATUS_KEYS.HIRED]: 'Hired'
}

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
    WARN: 'warning',
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
            VIDEO: ['mp4', 'm4v', 'mov', 'wmv', 'avi', 'mpg', 'webm'],
            IMAGE: ['png', 'jpeg', 'jpg', 'gif'],
            FILE: ['doc', 'docx', 'pdf', 'xls', 'xlsx', 'ppt', 'pptx', 'twb', 'twbx', 'pages', 'numbers', 'key', 'gdoc', 'gslides', 'gsheet']
        },
        APPLICATION_STATUS_KEYS,
        APPLICATION_STATUS,
        CANDIDATE_SUPPORT_EMAIL: 'community@uprove.co',
        CONTENT_TYPES,
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
        JOB_STATUS: {
            CLOSED: 'CLOSED',
            PAUSED: 'PAUSED',
            OPEN: 'OPEN',
            DRAFT: 'DRAFT'
        },
        LOOM_API_KEY: 'db47f7c0-e863-4ed8-ac6e-2c9872ad5c00',
        PROJECT_STATUSES,
        SEVERITY,
        SKILL_LEVEL: {
            1: {
                title: 'Entry-Intermediate Level',
                description: 'Comparable with 0-5 years experience',
            },
            2: {
                title: 'Mid-Senior Level',
                description: 'Comparable with 6+ years experience',
            },
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

export {
    globalData as default, APPLICATION_STATUS, APPLICATION_STATUS_KEYS, CONTENT_TYPES, DEGREE_OPTIONS,
    ORGANIZATION_TYPES, PROFILE_SECTIONS, PROJECT_EVAL_CUTOFFS, PROJECT_STATUSES,
    REMOTE_BITS, SEVERITY, TAG_TYPES, USER_BITS
};