import Data from '../../../utils/data';
import profileIcon from '../../../../images/profile_icon.svg';
import ProfilePage from './ProfilePage.vue';
import Vue from 'vue';


const EDUCATION_PLACEHOLDER_KEY = 'EDUCATION';

const appData = $('#vue-container').data();
const getMediaType = (mediaItem) => {
    const re = RegExp('^(video|image|application).*$');
    const match = mediaItem.post_mime_type.match(re);
    if (match) {
        return (match[1] === 'application') ? 'file' : match[1];
    }
    return null;
}

// Allow for globally listening for events
const eventBus = new Vue({
    methods: {
        saveContent(url, data, cfg = {}) {
            // If this is a new item, make sure it's in publish status so it's returned on get query
            if (cfg.method === 'POST') {
                data.status = 'publish';
            }
            const request = Object.assign({
                url,
                method: 'PUT',
                data,
                beforeSend(xhr) {
                    xhr.setRequestHeader('X-WP-Nonce', wpApi.nonce);
                },
                error({responseJSON, status}) {
                    console.log(`${status} - ${responseJSON.code}: ${responseJSON.message}`);
                },
            }, cfg);
            const ajaxRequest = $.ajax(request);

            // The first delete request only soft delete's. Need to send a second request to delete permanently
            if (cfg.method === 'DELETE') {
                $.ajax(request);
            }
            return ajaxRequest;
        },
        getUserContent(url, successFn, cfg = {}) {
            return new Promise((resolve, reject) => {
                $.ajax(Object.assign({
                    url,
                    data: {
                        per_page: 100,
                        author: appData.author_id | -2
                    },
                    success(result) {
                        successFn(result);
                        resolve(result);
                    },
                    error({responseJSON, status}) {
                        console.log(`${status} - ${responseJSON.code}: ${responseJSON.message}`);
                        reject();
                    },
                }, cfg));
            })
        },
        createMediaItem(file) {
            // Need to save media to the native wordpress media library before linking to Pods objects
            return new Promise((resolve, reject) => {
                const url = `${wpApi.root}media`;
                const formData = new FormData();
                formData.append('file', file);
                this.saveContent(url, formData, {
                    method: 'POST',
                    processData: false,
                    contentType: false,
                    cache: false,
                    error({responseJSON, status}) {
                        console.log(`${status} - ${responseJSON.code}: ${responseJSON.message}`);
                        reject();
                    },
                    success(mediaData) { resolve(mediaData.id); },
                });
            });
        },
        loadContent(contentTypes) {
            const loaders = [];
            contentTypes.forEach((contentType) => {
                loaders.push(loaderTypes[contentType]());
            })
            return Promise.all(loaders);
        }
    },
});

$(window).on('resize', (e) => {
    store.commit('updateScreenSize');
    eventBus.$emit('resize', e);
});

const getEducation = (contentItems = {}) => {
    for (const [key, contentItem] of Object.entries(contentItems)) {
        if(contentItem.post_type === 'education') {
            return [key, contentItem];
        }
    }
    return [null, null];
};

const getEducationId = (educationContentItems) => {
    if (!educationContentItems || !educationContentItems.length) {
        return EDUCATION_PLACEHOLDER_KEY;
    }
    const educationItemIds = educationContentItems.map((item) => item.ID)
    educationItemIds.sort();
    return educationItemIds.join('&');
};

const store = new Vuex.Store({
    state() {
        return {
            profileId: appData.profile_id,
            profilePicture: null,
            profile: {},
            content: {
                // Add a default education content to start in case no education content items are populated
                [EDUCATION_PLACEHOLDER_KEY]: {
                    post_type: 'education',
                    post_title: 'Education',
                    ID: EDUCATION_PLACEHOLDER_KEY,
                    contentItems: []
                }
            },
            media: [],
            highlightIds: [],
            degreeTypes: [
                {type: 'Associate of Arts'},
                {type: 'Associate of Science'},
                {type: 'Associate of Applied Science'},
                {type: 'Bachelor of Arts'},
                {type: 'Bachelor of Science'},
                {type: 'Master of Arts'},
                {type: 'Master of Science'},
                {type: 'Master of Business Administration'},
                {type: 'Doctoral Degree'},
                {type: 'Doctor of Medicine'},
                {type: 'Juris Doctor'},
            ],
            isOwner: Boolean(appData.is_owner),
            dateFormat: Data.dateFormat,
            crudUrlProfile: `${wpApi.root}profile/${appData.profile_id}`,
            crudBase: `${wpApi.root}`,
            eventBus: eventBus,
            isMobileDevice: $(window).width() <= 768
        }
    },
    mutations: {
        // Content
        addOrUpdateEducationItem(state, educationItem) {
            const [key, education] = getEducation(state.content);
            const serializedItem = Object.assign(
                _.pick(educationItem, ['school_name', 'degree_subject', 'degree_type']),
                {
                    ID: String(educationItem.ID || educationItem.id),
                    start_date: Data.convertToDayJS(educationItem.start_date),
                    end_date: Data.convertToDayJS(educationItem.end_date),
                    logoPicId: parseInt(educationItem.school_logo.ID),
                    guid: educationItem.school_logo.guid,
                    activities: Data.unescapeHTML(educationItem.activities)
                }
            );
            
            const currentContentItemIdx = education.contentItems.findIndex((item) => item.ID === serializedItem.ID);
            // This education item already exists. We're just updating it
            if (currentContentItemIdx !== -1) {
                education.contentItems[currentContentItemIdx] = serializedItem;
            } else {
                // Otherwise add new education item
                delete state.content[key];
                education.contentItems.push(serializedItem);

                // Sort education items in descending chronological order
                education.contentItems.sort((firstItem, secondItem) => {
                    if (firstItem.start_date.isBefore(secondItem.start_date)) {
                        return 1;
                    } else if (firstItem.endDate && firstItem.endDate.isBefore(secondItem.end_date)) {
                        return 0;
                    } else {
                        return -1;
                    }
                });

                // Generate the new key for all education items and update the state's content
                const newKey = getEducationId(education.contentItems);
                education.ID = newKey;
                state.content[newKey] = education;

                // If education is currently displayed, update it with new changes
                const educationSelectionIdx = state.highlightIds.indexOf(key);
                if (educationSelectionIdx !== -1) {
                    state.highlightIds[educationSelectionIdx] = newKey;
                    state.highlightIds = [...state.highlightIds];
                    const data = {highlight_ids: state.highlightIds.join(',')};
                    eventBus.saveContent(state.crudUrlProfile, data);
                }
            }

            // Need to reassign all of content for Vue's reactivity to work
            // It doesn't check for mutations within objects
            state.content = {...state.content};
        },
        removeEducationItem(state, educationItemId) {
            // Remove item from education object
            const [key, education] = getEducation(state.content);
            education.contentItems = education.contentItems.filter((contentItem) => contentItem.ID !== educationItemId);
            
            // Remove the old reference to education
            delete state.content[key];

            // Generate and set new education ID
            const newKey = getEducationId(education.contentItems);
            education.ID = newKey;
            state.content[newKey] = education;

            // If education is currently displayed, update it with new changes
            const educationSelectionIdx = state.highlightIds.indexOf(key);
            if (educationSelectionIdx !== -1) {
                state.highlightIds[educationSelectionIdx] = newKey;
                state.highlightIds = [...state.highlightIds];
                const data = {highlight_ids: state.highlightIds.join(',')};
                eventBus.saveContent(state.crudUrlProfile, data);
            }

            // Need to reassign all of content for Vue's reactivity to work
            // It doesn't check for mutations within objects
            state.content = {...state.content};
        },
        addOrUpdateVideoItem(state, videoItem) {
            const serializedItem = {
                ID: String(videoItem.ID || videoItem.id),
                description: videoItem.description,
                post_title: videoItem.post_title || Data.unescapeHTML(videoItem.title.rendered),
                post_type: videoItem.post_type || videoItem.type,
                created_dt: Data.convertToDayJS(videoItem.date, false),
                modified_dt: Data.convertToDayJS(videoItem.modified, false),
                mediaGuid: videoItem.video.guid,
                mediaId: parseInt(videoItem.video.ID),
                mediaType: getMediaType(videoItem.video)
            };

            // Need to reassign all of content for Vue's reactivity to work
            // It doesn't check for mutations within objects
            state.content = {
                ...state.content,
                [serializedItem.ID]: serializedItem
            }
        },
        addOrUpdateProjectItem(state, projectItem) {
            const serializedItem = {
                ID: String(projectItem.ID || projectItem.id),
                description: projectItem.description,
                post_title: projectItem.post_title || Data.unescapeHTML(projectItem.title.rendered),
                post_type: projectItem.post_type || projectItem.type,
                created_dt: Data.convertToDayJS(projectItem.date, false),
                modified_dt: Data.convertToDayJS(projectItem.modified, false),
                mediaGuid: (projectItem.media) ? projectItem.media.guid : null,
                mediaId: (projectItem.media) ? parseInt(projectItem.media.ID) : null,
                mediaType: (projectItem.media) ? getMediaType(projectItem.media) : null,
                files: (projectItem.files || []).map((file) => (
                    {id: parseInt(file.ID), guid: file.guid, type: getMediaType(file), title: file.post_title}
                ))
            };

            // Need to reassign all of content for Vue's reactivity to work
            // It doesn't check for mutations within objects
            state.content = {
                ...state.content,
                [serializedItem.ID]: serializedItem
            }
        },
        addOrUpdateExperienceItem(state, experienceItem) {
            const serializedItem = Object.assign(_.pick(experienceItem, ['position_title', 'employment_type', 'company', 'description']), {
                ID: String(experienceItem.ID || experienceItem.id),
                post_title: experienceItem.post_title || Data.unescapeHTML(experienceItem.title.rendered),
                post_type: experienceItem.post_type || experienceItem.type,
                start_date: Data.convertToDayJS(experienceItem.start_date, false),
                end_date: Data.convertToDayJS(experienceItem.end_date, false),
            });

            if (experienceItem.logo) {
                serializedItem.logo = {
                    id: parseInt(experienceItem.logo.ID),
                    guid: experienceItem.logo.guid
                }
            }

            state.content = {
                ...state.content,
                [serializedItem.ID]: serializedItem
            }
        },

        updateProfile(state, profile) {
            Object.assign(state.profile, profile);
            state.profilePicture = profile.profile_picture.guid || profileIcon;
            state.profile.sections = (state.profile.sections) ? JSON.parse(state.profile.sections) : [];
            state.profile = {...state.profile};
        },
        updateMedia(state, media) {
            state.media = media;
        },
        setHighlightIds(state, highlightIds) {
            state.highlightIds = highlightIds;
        },
        addHighlightId(state, {id}) {
            state.highlightIds.push(id);
            const data = {highlight_ids: state.highlightIds.join(',')};
            eventBus.saveContent(state.crudUrlProfile, data);
            state.profile = {...state.profile};
        },
        removeHighlightId(state, {id}) {
            state.highlightIds = state.highlightIds.filter((highlightId) => highlightId !== id);
            eventBus.saveContent(state.crudUrlProfile, {highlight_ids: state.highlightIds.join(',')});
            state.profile = {...state.profile};
        },
        moveHighlightId(state, {itemIdx, direction}) {
            const id = state.highlightIds[itemIdx];
            state.highlightIds.splice(itemIdx, 1);
            state.highlightIds.splice(itemIdx + direction, 0, id);
            eventBus.saveContent(state.crudUrlProfile, {highlight_ids: state.highlightIds.join(',')});
            state.profile = {...state.profile};
        },
        addSectionId(state, {id, sectionIdx}) {
            state.profile.sections[sectionIdx].ids.push(id);
            eventBus.saveContent(state.crudUrlProfile, {sections: JSON.stringify(state.profile.sections)});
            state.profile = {...state.profile};
        },
        removeSectionId(state, {id, sectionIdx}) {
            const ids = state.profile.sections[sectionIdx].ids.filter((contentId) => contentId !== id);
            state.profile.sections[sectionIdx].ids = ids;
            eventBus.saveContent(state.crudUrlProfile, {sections: JSON.stringify(state.profile.sections)});
            state.profile = {...state.profile};
        },
        moveSectionId(state, {itemIdx, sectionIdx, direction}) {
            const id = state.profile.sections[sectionIdx].ids[itemIdx];
            state.profile.sections[sectionIdx].ids.splice(itemIdx, 1);
            state.profile.sections[sectionIdx].ids.splice(itemIdx + direction, 0, id);
            eventBus.saveContent(state.crudUrlProfile, {sections: JSON.stringify(state.profile.sections)});
            state.profile = {...state.profile};
        },
        removeSection(state, sectionIdx) {
            state.profile.sections.splice(sectionIdx, 1)
            eventBus.saveContent(state.crudUrlProfile, {sections: JSON.stringify(state.profile.sections)});
            state.profile = {...state.profile};
        },
        moveSection(state, {sectionIdx, direction}) {
            const section = state.profile.sections[sectionIdx];
            state.profile.sections.splice(sectionIdx, 1);
            state.profile.sections.splice(sectionIdx + direction, 0, section);
            eventBus.saveContent(state.crudUrlProfile, {sections: JSON.stringify(state.profile.sections)});
            state.profile = {...state.profile};
        },
        updateScreenSize(state) {
            state.isMobileDevice = $(window).width() <= 768;
        }
    },
    getters: {
        // Content could be one item (like a video) or a group of content items (like all education)
        getContentItem: (state) => (contentId) => {
            return state.content[contentId];
        },
        getLastContentType: (state) => (contentType) => {
            const content = (Object.values(state.content) || []).filter((contentItem) => contentItem.post_type === contentType);
            if (!content.length) {
                return null;
            }
            // Sort in descending chronological order
            content.sort((firstItem, secondItem) => (firstItem.created_dt.isBefore(secondItem.created_dt)) ? 1 : -1)
            return content[0];
        }
    }
});

// Load profile
const getProfileLoader = () => {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: store.state.crudUrlProfile,
            success(result) {
                const highlightIds = (result.highlight_ids) ? Data.parseIdString(result.highlight_ids) : [];
        
                store.commit('updateProfile', result);
                store.commit('setHighlightIds', highlightIds);
                resolve(result);
            },
            error({responseJSON, status}) {
                console.log(`${status} - ${responseJSON.code}: ${responseJSON.message}`);
                reject();
            },
        });
    });
}

// Load media
const mediaSuccessFn = (result) => {
    const media = result.map(({id, guid, mime_type, title, date, modified}) => {
        return {
            id,
            guid: guid.rendered,
            type: getMediaType({post_mime_type: mime_type}),
            title: Data.unescapeHTML(title.rendered),
            created_dt: Data.convertToDayJS(date, false),
            modified_dt: Data.convertToDayJS(modified, false)
        };
    });
    store.commit('updateMedia', media);
}
const getMediaLoader = () => eventBus.getUserContent(`${store.state.crudBase}media`, mediaSuccessFn);

// Load education
const educationSuccessFn = (result) => {
    (result || []).forEach((educationItem) => { store.commit('addOrUpdateEducationItem', educationItem); })
}
const getEducationLoader = () => eventBus.getUserContent(`${store.state.crudBase}education`, educationSuccessFn);

// Load video content
const videoSuccessFn = (result) => {
    (result || []).forEach((videoItem) => { store.commit('addOrUpdateVideoItem', videoItem); });
}
const getVideoLoader = () => eventBus.getUserContent(`${store.state.crudBase}video`, videoSuccessFn);

// Load project content
const projectSuccessFn = (result) => {
    (result || []).forEach((projectItem) => { store.commit('addOrUpdateProjectItem', projectItem); });
}
const getProjectLoader = () => eventBus.getUserContent(`${store.state.crudBase}project`, projectSuccessFn);

// Load experience content
const experienceSuccessFn = (result) => {
    (result || []).forEach((experienceItem) => { store.commit('addOrUpdateExperienceItem', experienceItem); });
}
const getExperienceLoader = () => eventBus.getUserContent(`${store.state.crudBase}experience`, experienceSuccessFn);

// Print all available routes
// $.ajax({
//     url: wpApi.root,
//     success( result ) {
//         console.log(result.routes);
//     }
// });

$.ajax({
    url: 'http://uprove.local/wp-json/uprove/login',
    method: 'POST',
    data: {username: 'todd'},
    success( result ) {
        console.log(result);
    }
});
const loaderTypes = {
    profile: getProfileLoader,
    media: getMediaLoader,
    education: getEducationLoader,
    experience: getExperienceLoader,
    video: getVideoLoader,
    project: getProjectLoader
}

// Instantiate profile page
const loadPage = (initData) => {
    eventBus.loadContent(['profile', 'media', 'education', 'experience', 'video', 'project']).then((values) => {
        Vue.createApp({
            el: '#vue-container',
            store,
            render(h){
                return h(ProfilePage, {});
            }
        });
    });
}

export default loadPage;
