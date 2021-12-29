<template>
    <BaseModal
        :modalId="modalName"
        :modalTitle="(formData.id) ? 'Edit blog' : 'Create new blog'"
        :primaryButtonText="(formData.id) ? 'Save changes' : 'Create blog'"
        :isAllowDelete="Boolean(formData.id)"
        :isLargeDisplay="true"
        @saveChange="saveChange($event)"
        @deleteObject="deleteObject($event)"
    >
        <div class="mb-3">
            <label for="blogTitle" class="form-label">Title</label>
            <input type="text" class="form-control" placeholder="Required" id="blogTitle" v-model="formData.title">
        </div>
        <div class="mb-3">
            <label for="blogAuthor" class="form-label">Author</label>
            <InputSelectize
                ref="blogAuthor"
                elId="modalBlogAuthor"
                :isParseAsInt="true"
                placeholder="Required" :cfg="authorsCfg" @selected="formData.authorId = $event"
            />
        </div>
        <div class="mb-3">
            <label for="blogPublishDate" class="form-label">Publish Date <InfoToolTip :content="TOOLTIPS.blogPublishDate" :elId="getNewElUid()"/></label>
            <input type="date" class="form-control" id="blogPublishDate" v-model="formData.publishDate">
        </div>
        <div class="mb-3">
            <label for="blogTags" class="form-label">Tags</label>
            <InputSelectize
                ref="blogTags"
                elId="modalBlogTags"
                placeholder="Optional" :cfg="blogTagsCfg" @selected="formData.blogTags = $event"
            />
        </div>
        <div class="mb-3">
            <InputOrViewMedia
                inputId="blogPicture"
                :mediaTypes="['image']"
                itemLabel="picture"
                :currentItem="formData.picture"
                @selected="formData.picture = $event"
            />
        </div>
        <div class="mb-3">
            <label for="blogPost" class="form-label">Post</label>
            <InputWsiwyg v-model="formData.post" elId="blogPost" placeholder="Write post..."/>
        </div>
    </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal";
import InfoToolTip from "../components/InfoToolTip";
import InputOrViewMedia from "../inputs/InputOrViewMedia";
import InputSelectize from "../inputs/InputSelectize";
import InputWsiwyg from "../inputs/InputWsiwyg";
import dataUtil from "../../utils/data";

export default {
    name: "EditBlogModal.vue",
    extends: BaseModal,
    inheritAttrs: false,
    components: {BaseModal, InfoToolTip, InputOrViewMedia, InputSelectize, InputWsiwyg},
    data() {
        return {
            modalName: 'editBlogModal',
            crudUrl: 'blog/',
            isUpdateData: true,
            initDataKey: 'blogs',
            requiredFields: {
                title: '#blogTitle',
                post: '#blogPost',
                authorId: null  // Set on mounted
            },
            mediaFields: ['picture'],
        }
    },
    computed: {
        authorsCfg() {
            return {
                maxItems: 1,
                options: dataUtil.sortBy(this.initData.authors.map((a) => ({value: a.id, text: `${a.firstName} ${a.lastName}`})), 'text')
            };
        },
        blogTagsCfg() {
            return {
                create: (text) => ({value: text, text}),
                plugins: ['remove_button'],
                maxItems: null,
                options: dataUtil.sortBy(this.initData.blogTags.map((t) => ({value: t.name, text: t.name})), 'text')
            };
        }
    },
    methods: {
        processRawData(rawData) {
            this.requiredFields.authorId = this.$refs.blogAuthor.targetEl;
            return rawData;
        },
        setFormFields() {
            this.$refs.blogAuthor.elSel.setValue(this.formData.author.id);
            this.$refs.blogTags.elSel.setValue(this.formData.blogTags.map((t) => t.name));
        },
    }
}
</script>