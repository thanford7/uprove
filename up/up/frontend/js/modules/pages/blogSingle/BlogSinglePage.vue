<template>
    <div class="container-lg blog-post">
        <div class="row mt-3 mb-3">
            <a href="/blog/">Back to blog posts</a>
            <div class="col image-wrap">
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
    </div>
    <EditBlogModal v-if="isSuperUser"/>
</template>

<script>
import EditBlogModal from "../../modals/EditBlogModal";
export default {
    name: "BlogSinglePage",
    components: {EditBlogModal},
    methods: {
        getBlogUrl(blog) {
            return `https://www.uprove.co/blog/${blog.id}/`;
        },
    }
}
</script>