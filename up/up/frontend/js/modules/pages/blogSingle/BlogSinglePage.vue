<template>
    <BasePage class="blog-post">
        <div class="row mt-3 mb-3">
            <a href="/blog/">Back to blog posts</a>
            <div class="col card-custom" :class="(isMobile) ? '' : 'image-wrap'">
                <img v-if="initData.blog.picture" :src="initData.blog.picture" class="blog-img">
                <h2>
                    {{initData.blog.title}}
                    <button v-if="isSuperUser" type="button" class="btn btn-secondary" @click="eventBus.emit('open:editBlogModal', initData.blog)">
                        Edit post
                    </button>
                </h2>
                <div v-html="initData.blog.post"></div>
                <div>
                    <a :href="`https://www.twitter.com/share?text=${initData.blog.title}&url=${getBlogUrl(initData.blog)}`" target="_blank">
                        <i class="fab fa-twitter-square"></i>&nbsp;Share on Twitter
                    </a>&nbsp;
                    <a :href="`https://www.linkedin.com/shareArticle?url=${getBlogUrl(initData.blog)}`" target="_blank">
                        <i class="fab fa-linkedin"></i>&nbsp;Share on LinkedIn
                    </a>
                </div>
            </div>
        </div>
    </BasePage>
    <EditBlogModal v-if="isSuperUser" newInitDataKey="blog" newDeleteRedirectUrl="/blog/"/>
</template>

<script>
import EditBlogModal from "../../modals/EditBlogModal";
import BasePage from "../base/BasePage";
export default {
    name: "BlogSinglePage",
    components: {BasePage, EditBlogModal},
    methods: {
        getBlogUrl(blog) {
            return `https://www.uprove.co/blog/${blog.id}/`;
        },
    }
}
</script>