<template>
    <div>
        <div class="mb-3">
            <label for="formProfileName" class="form-label">Company or organization</label>
            <input type="text" class="form-control" placeholder="Add name..." v-model="formData.company">
        </div>
        <div class="mb-3">
            <label class="form-label">Logo</label>
            <InputSelectOrUploadMedia
                ref="logoPic"
                :currentMediaIds="(contentItem.logo) ? [contentItem.logo.id] : null"
                :mediaTypes="['image']"
                placeholderDescription="Logo picture"
            />
        </div>
        <div class="mb-3">
            <label for="positionTitle" class="form-label">Position title</label>
            <input type="text" class="form-control" placeholder="Add title..." v-model="formData.position_title">
        </div>
        <div class="mb-3">
            <label for="employmentType" class="form-label">Employment type</label>
            <InputSelectize 
                :currentItem="contentItem.employment_type"
                :cfg="employmentTypeSelCfg"
                @selected="formData.employment_type = $event"
                placeholder="Select type..."
            />
        </div>
        <div class="row mb-3">
            <div class="col-md-3">
                <label class="form-label" for="employmentStartDate">Start date</label>
                <InputMonthYear v-model="formData.start_date"/>
            </div>
            <div class="col-md-3">
                <label class="form-label" for="employmentEndDate">End date</label>
                <InputMonthYear v-model="formData.end_date"/>
            </div>
        </div>
        <div class="mb-3">
            <label class="form-label" for="employmentDescription">Description</label>
            <InputWsiwyg
                placeholder="Add description of position..."
                v-model="formData.description"
            />
        </div>
    </div>
</template>
<script>
import {mapState} from 'vuex';
import dataUtil from '../../utils/data';
import InputMonthYear from '../inputs/InputMonthYear.vue';
import InputSelectize from '../inputs/InputSelectize.vue';
import InputSelectOrUploadMedia from '../inputs/InputSelectOrUploadMedia.vue';
import InputWsiwyg from '../inputs/InputWsiwyg.vue';

export default {
    data() {
        return {
            contentId: null,

            inputs: {
                company: {
                    setter: () => this.contentItem.company
                },
                position_title: {
                    setter: () => this.contentItem.position_title
                },
                start_date: {
                    setter: () => this.contentItem.start_date
                },
                end_date: {
                    setter: () => this.contentItem.end_date
                },
                description: {
                    setter: () => this.contentItem.description
                }
            },

            employmentTypeSelCfg: {
                options: [
                    {name: 'Full-time'},
                    {name: 'Part-time'},
                    {name: 'Self-employed'},
                    {name: 'Contracted'},
                    {name: 'Internship'}
                ],
                maxItems: 1,
                valueField: 'name',
                labelField: 'name'
            }
        }
    },
    components: {InputMonthYear, InputSelectize, InputSelectOrUploadMedia, InputWsiwyg},
    computed: {
        ...mapState({
            eventBus: 'eventBus'
        }),
        formData() {
            const formData = {};
            Object.entries(this.inputs).forEach(([input, cfg]) => {
                formData[input] = cfg.setter();
            });
            return formData;
        }
    },
    props: {
        contentItem: {
            type: Object,
            default: () => ({})
        },
    },
    methods: {
        readForm() {
            const formData = {...this.formData};
            formData.start_date = dataUtil.formatDate(formData.start_date, {isReturnNull: true});
            formData.end_date = dataUtil.formatDate(formData.end_date, {isReturnNull: true});
            formData.title = formData.company;
            return formData;
        },
        getPreSaveChange() {
            const formData = this.readForm();
            const {uploadValue, existingValue} = this.$refs.logoPic.getValue();
            if (uploadValue) {
                return this.eventBus.createMediaItem(uploadValue).then((mediaItem) => Object.assign(formData, {logo: mediaItem.id}));
            } else {
                return new Promise((resolve) => {
                    resolve(Object.assign(formData, {logo: existingValue}));
                })
            }
        },
    }
}
</script>