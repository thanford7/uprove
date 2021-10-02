<template>
    <BaseModal
        modalId="addContentModal"
        modalTitle="Add content"
        :isLargeDisplay="true"
        @saveChange="saveChange"
    >
        <div>
            <div>
                <label for="selectContent" class="form-label">Existing content</label>
                <ContentSelectize :contentSection="contentSection" :currentContentIds="contentSectionIds" @selected="selectedContentId = $event"/>
            </div>
            <div :class="(isNewItem) ? 'modal-body-banner modal-body-banner--top' : ''">
                <label for="addContentType" class="form-label">New content</label>
                <InputSelectize elId="addContentType" placeholder="Select content type" :cfg="addContentCfg" @selected="addContentType = $event"/>
            </div>
        </div>
        <div id="newItemForm" v-if="addContentType">
            <MediaFormContent v-if="['video', 'project'].includes(addContentType)" :contentType="addContentType" :allowedBannerMediaTypes="allowedBannerMediaTypes" ref="formContentMedia"/>
            <ExperienceFormContent v-if="addContentType === 'experience'" ref="formContentExperience"/>
        </div>
        <div class="modal-body-banner modal-body-banner--bottom"><a id="newItemToggle" href="#" @click="toggleAddNewItem(!isNewItem)"><font-awesome-icon :icon="['fas', 'plus-circle']"/> Add new content</a></div>
    </BaseModal>
</template>
<script>
import Modal from 'bootstrap/js/dist/modal';
import {mapGetters, mapState} from 'vuex';
import BaseModal from './BaseModal.vue';
import ContentSelectize from '../inputs/ContentSelectize.vue';
import ExperienceFormContent from './ExperienceFormContent.vue';
import MediaFormContent from './MediaFormContent.vue';
import InputSelectize from '../inputs/InputSelectize.vue';

export default {
    extends: BaseModal,
    components: {BaseModal, ContentSelectize, ExperienceFormContent, InputSelectize, MediaFormContent},
    inheritAttrs: false,
    data() {
        return {
            contentSection: null,  // Either highlights or section. The highlights section is at the top of the page and may restrict content types
            contentSectionOrder: null, // For all "section" content sections, the contentSectionOrder is used to save updates to the appropriate section
            modal$: null,
            selectedContentId: null,
            isNewItem: false,
            newItemToggle$: null,
            selectContent$: null,
            addContentSel$: null,
            addContentCfg: {
                maxItems: 1,
                options: [
                    {value: 'experience', text: 'Experience'},
                    {value: 'project', text: 'Project'},
                    {value: 'video', text: 'Video'},
                ]
            },
            addContentType: null
        }
    },
    computed: {
        ...mapState({
            eventBus: 'eventBus',
            profile: 'profile',
            crudUrl(state) {
                return `${state.crudBase}${this.addContentType}`;
            }
        }),
        ...mapGetters({
            getLastContentType: 'getLastContentType'
        }),
        allowedBannerMediaTypes() {
            return (this.addContentType === 'video') ? ['video'] : ['video', 'image'];
        },
        contentSectionIds() {
            if (this.contentSectionOrder) {
                return this.profile.sections[this.contentSectionOrder].ids
            }
            return [];
        }
    },
    methods: {
        hookEvents() {
            this.eventBus.$on('open:addContentModal', (contentSection, contentSectionOrder) => {
                this.contentSection = contentSection;
                this.contentSectionOrder = contentSectionOrder;
                this.modal$.show();
            });
        },
        readForm() {
            return {}; // Form data is returned in getPreSaveChange
        },
        getPreSaveChange() {
            let formContent;
            if (['video', 'project'].includes(this.addContentType)) {
                formContent = this.$refs.formContentMedia;
            } else if (this.addContentType === 'experience') {
                formContent = this.$refs.formContentExperience;
            }
            return formContent.getPreSaveChange().then((content) => {
                if (addContentType === 'video' && content.media) {
                    content.video = content.media;
                }
                return content;
            });
        },
        saveChange() {
            if (!this.isNewItem && this.selectedContentId) {
                this.$store.commit(`add${_.capitalize(this.contentSection)}Id`, {id: this.selectedContentId, sectionIdx: this.contentSectionOrder});
            } else {
                this.$super(BaseModal).saveChange({method: 'POST'});
            }
        },
        onSaveSuccess(newContentItem) {
            this.eventBus.loadContent(['media', this.addContentType]).then(() => {
                const lastContentItem = this.getLastContentType(this.addContentType);
                this.$store.commit(`add${_.capitalize(this.contentSection)}Id`, {id: lastContentItem.ID});;
            });
        },
        toggleAddNewItem(isNewItem) {
            this.isNewItem = isNewItem;
            this.newItemToggle$.text((isNewItem) ? 'Select existing content' : 'Add new content');
            this.selectContent$.toggle(!isNewItem);
            this.addContentSel$.toggle(isNewItem);
            $('#newItemForm').toggle(isNewItem);
        },
    },
    mounted() {
        if(!this.modal$) {
            this.modal$ = new Modal($('#addContentModal'));
        }
        this.addContentSel$ = $('#addContentType').parent();
        this.selectContent$ = $('#selectContent').parent();
        this.newItemToggle$ = $('#newItemToggle');
        this.toggleAddNewItem(this.isNewItem);
    },
}
</script>
