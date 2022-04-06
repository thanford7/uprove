<template>
    <BasePage headerTitle="Blog" class="blog-post">
        <div class="row mb-3" :class="(isMobile) ? 'mobile-top' : ''">
            <div class="col-md-8 pe-md-4 card-custom" :class="(isMobile) ? '' : 'image-wrap'">
                <template v-if="latestPost">
                    <img v-if="latestPost.picture" :src="latestPost.picture" class="blog-img">
                    <h3>
                        {{latestPost.title}}
                        <button v-if="isSuperUser" type="button" class="btn btn-secondary" @click="eventBus.emit('open:editBlogModal', latestPost)">
                            Edit post
                        </button>
                    </h3>
                    <div v-html="latestPost.post"></div>
                    <div>
                        <a :href="`https://www.twitter.com/share?text=${latestPost.title}&url=${getBlogUrl(latestPost)}`" target="_blank">
                            <i class="fab fa-twitter-square"></i>&nbsp;Share on Twitter
                        </a>&nbsp;
                        <a :href="`https://www.linkedin.com/shareArticle?url=${getBlogUrl(latestPost)}`" target="_blank">
                            <i class="fab fa-linkedin"></i>&nbsp;Share on LinkedIn
                        </a>
                    </div>
                </template>
            </div>
            <div class="col-md-3 sidebar mb-3" :class="(isMobile) ? 'mobile-side-margin' : ''">
                <button v-if="isSuperUser" type="button" class="btn btn-primary w-100 mb-3" @click="eventBus.emit('open:editBlogModal')">
                    Add blog post
                </button>
                <div v-if="isSuperUser && unpublishedPosts.length" class="mb-3">
                    <h4>Edit unpublished post</h4>
                    <div v-for="blog in unpublishedPosts">
                        <a href="#" @click="eventBus.emit('open:editBlogModal', blog)">{{blog.title}}</a>
                    </div>
                </div>
                <h4>Recent posts</h4>
                <ul v-for="blog in publishedPosts">
                    <li>
                        <a :href="`/blog/${blog.id}/`">{{blog.title}}</a>
                    </li>
                </ul>
            </div>
        </div>
    </BasePage>
    <EditBlogModal v-if="isSuperUser" newInitDataKey="blogs"/>
</template>

<script>
import dataUtil from "../../../utils/data";
import EditBlogModal from "../../modals/EditBlogModal";
import BasePage from "../base/BasePage";

export default {
    name: "BlogPage.vue",
    components: {BasePage, EditBlogModal},
    computed: {
        unpublishedPosts() {
            return this.initData.blogs.filter((b) => !b.isPublished);
        },
        publishedPosts() {
            return this.sortByDate(this.initData.blogs.filter((b) => b.isPublished));
        },
        latestPost() {
            if (!this.publishedPosts.length) {
                return null;
            }
            return this.publishedPosts[0];
        }
    },
    methods: {
        getBlogUrl(blog) {
            return `https://www.uprove.co/blog/${blog.id}/`;
        },
        sortByDate(posts) {
            // Latest first
            return posts.sort((a, b) =>  dataUtil.convertToDayJS(b.publishDate).diff(a.publishDate, 'day'));
        }
    }
}
</script>