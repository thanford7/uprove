<template>
    <BaseModal
        :modalId="modalName"
        modalTitle="Edit education"
        :isScrollable="true"
        :isLargeDisplay="true"
        @saveChange="saveChange"
    >
        <div v-for="(data, educationItemId) in formData" class="form-section" :key="educationItemId">
            <div class="mb-3">
                <label :for="`formSchoolName-${educationItemId}`" class="form-label">School name</label>
                <input type="text" class="form-control" placeholder="Add school name..." :id="`formSchoolName-${educationItemId}`" v-model="data.school_name">
            </div>
            <div class="mb-3">
                <label class="form-label">School logo</label>
                <MediaSelectize 
                    :elId="`formImageSel-${educationItemId}`" 
                    :currentMediaIds="[data.logoPicId]"
                    :mediaTypes="['image']"
                    placeholder="Select logo image..."
                    @selected="data.selectedLogoPicId = $event" 
                />
                <InputMedia :elId="`formImageUpload-${educationItemId}`" :mediaTypes="['image']" @selected="imageUploadVals[educationItemId] = $event"/>
                <a href="#" :id="`formToggleImageUpload-${educationItemId}`" @click="toggleImageUpload(educationItemId)">Upload new logo</a>
            </div>
            <div class="row">
                <div class="col-md-3">
                    <label class="form-label" :for="`formStartDate-${educationItemId}`">Start date</label>
                    <InputMonthYear v-model="data.start_date"/>
                </div>
                <div class="col-md-3" :id="`formEndDate-${educationItemId}`">
                    <label class="form-label" :for="`formEndDate-${educationItemId}`">End date</label>
                    <InputMonthYear v-model="data.end_date"/>
                </div>
            </div>
            <div class="row mb-3"><div class="form-text">Start date is required, end date can be blank or in the future for expected completion.</div></div>
            <div class="mb-3">
                <label class="form-label" :for="`formDegreeType-${educationItemId}`">Degree type</label>
                <div :id="`formDegreeType-${educationItemId}`">
                    <select :id="`formDegreeTypeSel-${educationItemId}`" placeholder="Add degree type..."></select>
                </div>
            </div>
            <div class="mb-3">
                <label class="form-label" :for="`formDegreeSubject-${educationItemId}`">Degree subject</label>
                <input type="text" class="form-control" :id="`formDegreeSubject-${educationItemId}`" placeholder="Add degree subject..." v-model="data.degree_subject">
            </div>
            <div class="mb-3">
                <label class="form-label">Activities</label>
                <div :id="`formActivities-${educationItemId}`">
                    <InputWsiwyg placeholder="Add activities..." v-model="data.activities"/>
                </div>
            </div>
            <div class="mb-3">
                <a href="#" @click="deleteEducationItem(educationItemId)"><font-awesome-icon :icon="['fas', 'trash-alt']"/> Delete education</a>
            </div>
        </div>
        <div><a href="#" @click="addEducationItem"><font-awesome-icon :icon="['fas', 'plus-circle']"/> Add new education</a></div>
    </BaseModal>
</template>
<script>
import Modal from 'bootstrap/js/dist/modal';
import {mapGetters, mapState} from 'vuex';
import BaseModal from './BaseModal.vue';
import dataUtil from '../../utils/data';
import InputMedia from '../inputs/InputMedia.vue';
import InputMonthYear from '../inputs/InputMonthYear.vue';
import InputWsiwyg from '../inputs/InputWsiwyg.vue';
import MediaSelectize from '../inputs/MediaSelectize.vue';

export default {
    extends: BaseModal,
    data() {
        return {
            modalName: 'editEducationModal',
            contentId: null,
            newEducationItemIdPrefix: 'new-',
            newEducationItems: 0,
            contentItems: [],
            formData: {},
            inputs: {
                school_name: {
                    setter: (educationItem) => educationItem.school_name
                },
                logoPicId: {
                    setter: (educationItem) => educationItem.logoPicId
                },
                degree_type: {
                    setter: (educationItem) => educationItem.degree_type
                },
                degree_subject: {
                    setter: (educationItem) => educationItem.degree_subject
                },
                start_date: {
                    setter: (educationItem) => dataUtil.convertToDayJS(educationItem.start_date)
                },
                end_date: {
                    setter: (educationItem) => dataUtil.convertToDayJS(educationItem.end_date)
                },
                activities: {
                    setter: (educationItem) => educationItem.activities
                }
            },

            // Logo handling
            imageUploadVals: {},
        }
    },
    inheritAttrs: false,
    components: {BaseModal, InputMedia, InputMonthYear, InputWsiwyg, MediaSelectize},
    computed: {
        ...mapState({
            eventBus: 'eventBus',
            dateFormat: 'dateFormat',
            degreeTypes: 'degreeTypes',
            crudUrlMedia(state) {
                return `${state.crudBase}media`
            },
            crudBaseUrl(state) {
                return `${state.crudBase}education/`
            }
        }),
        ...mapGetters({
            getContentItem: 'getContentItem'
        })
    },
    watch: {
        contentItems(newEducationItems) {
            const newFormData = {};
            newEducationItems.forEach((educationItem) => {
                const educationItemData = this.formData[educationItem.ID] || {};
                Object.entries(this.inputs).forEach(([input, cfg]) => {
                    educationItemData[input] = cfg.setter(educationItem) || educationItemData[input];
                });
                newFormData[educationItem.ID] = educationItemData;
            });
            this.formData = newFormData;
        }
    },
    methods: {
        addEducationItem() {
            this.contentItems.push({ID: `${this.newEducationItemIdPrefix}${this.newEducationItems}`});
            this.newEducationItems++;
        },
        deleteEducationItem(educationItemId) {
            if(confirm('Are you sure you want to permanently delete this education item?')) {
                const url = `${this.crudBaseUrl}${educationItemId}`;
                this.eventBus.saveContent(url, null, {method: 'DELETE'});
                this.$store.commit('removeEducationItem', educationItemId);
                this.contentItems = this.contentItems.filter((contentItem) => contentItem.ID !== educationItemId);
            }
        },
        processFormData(data, imageData) {
            data.start_date = dataUtil.formatDate(data.start_date);
            data.end_date = dataUtil.formatDate(data.end_date, {isReturnNull: true});
            data.school_logo = data.selectedLogoPicId;
            return this.$super(BaseModal).processFormData(data, imageData);
        },
        onSaveSuccess(requestData, responseData) {
            this.$store.commit('addOrUpdateEducationItem', responseData);
        },
        hookEvents() {
            this.eventBus.$on('open:editEducationModal', (contentId) => {
                this.contentId = contentId;
                this.contentItems = [...this.getContentItem(this.contentId).contentItems];
                this.modal$.show();
            });
        },
        saveChange() {
            Object.entries(this.formData).forEach(([educationItemId, data]) => {
                // Save the uploaded image first if it exists
                const isUploadShown = $(`#formImageUpload-${educationItemId}`).css('display') !== 'none';
                const imageUploadData = this.imageUploadVals[educationItemId];
                let imagePromise;
                if (isUploadShown && imageUploadData) {
                    imagePromise = new Promise((resolve, reject) => {
                        this.createMediaImage(imageUploadData, resolve, reject);
                    });
                } else {
                    imagePromise = this.$super(BaseModal).getPreSaveChange();
                }

                imagePromise.then((imageData) => {
                    const requestData = this.processFormData(data, imageData);
                    const isNewItem = String(educationItemId).includes(this.newEducationItemIdPrefix);
                    const url = (isNewItem) ? this.crudBaseUrl : `${this.crudBaseUrl}${educationItemId}`;
                    this.eventBus.saveContent(url, requestData, {
                        method: (isNewItem) ? 'POST' : 'PUT',
                        success: (responseData) => {
                            this.onSaveSuccess(null, responseData);
                        },
                    });
                });
            });
        },
        createMediaImage(imageData, resolve, reject) {
            // Need to save images to the native wordpress media library before linking to Pods objects
            const formData = new FormData();
            formData.append('file', imageData);
            this.eventBus.saveContent(this.crudUrlMedia, formData, {
                method: 'POST',
                processData: false,
                contentType: false,
                cache: false,
                error({responseJSON, status}) {
                    console.log(`${status} - ${responseJSON.code}: ${responseJSON.message}`);
                    reject();
                },
                success(imageData) {
                    resolve({school_logo: imageData.id});
                },
            });
        },
        toggleImageUpload(educationItemId) {
            const upload$ = $(`#formImageUpload-${educationItemId}`);
            const sel$ = $(`#formImageSel-${educationItemId}`).parent().find('.selectize-control');
            const isUploadShown = upload$.css('display') !== 'none';
            const isSelShown = sel$.css('display') !== 'none';
            $(`#formToggleImageUpload-${educationItemId}`).text((isSelShown) ? 'Select existing logo' : 'Upload new logo');

            upload$.toggle(!isUploadShown);
            sel$.toggle(!isSelShown);
        },
    },
    updated() {
        Object.entries(this.formData).forEach(([educationItemId, educationItem]) => {
            const degreeTypeSel = $(`#formDegreeTypeSel-${educationItemId}`).selectize({
                options: this.degreeTypes,
                valueField: 'type',
                labelField: 'type',
                searchField: ['type'],
                maxItems: 1,
                create: true,
                persist: false,
                hideSelected: true
            })[0].selectize;

            // Add custom degree type if user has added one
            if(!this.degreeTypes.find((degreeType) => degreeType.type === educationItem.degree_type)) {
                degreeTypeSel.addOption({type: educationItem.degree_type})
            }

            degreeTypeSel.addItem(educationItem.degree_type, true);

            degreeTypeSel.on('blur', () => {
                educationItem.degree_type = degreeTypeSel.getValue();
            })
        });

        $('.input-image').toggle(false);
    }
}
</script>