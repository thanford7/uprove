<template>
    <BasePage class="blog-post">
        <div class="row mb-3 mt-5" :class="(isMobile) ? 'mobile-top' : ''">
            <div class="col-md-7 pe-md-4 card-custom card-custom--no-top-margin" :class="(isMobile) ? '' : 'image-wrap'">
                <template v-if="latestPost">
                    <img v-if="latestPost.picture" :src="latestPost.picture" class="blog-img">
                    <h5>
                        {{latestPost.title}}
                        <button v-if="isSuperUser" type="button" class="btn btn-secondary" @click="eventBus.emit('open:editBlogModal', latestPost)">
                            Edit post
                        </button>
                    </h5>
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
            <div class="col-md-4 sidebar mb-3" :class="(isMobile) ? 'mobile-side-margin' : ''">
                <button v-if="isSuperUser" type="button" class="btn btn-primary w-100 mb-3" @click="eventBus.emit('open:editBlogModal')">
                    Add blog post
                </button>
                <div v-if="isSuperUser && unpublishedPosts.length" class="mb-3">
                    <h4>Edit unpublished post</h4>
                    <div v-for="blog in unpublishedPosts">
                        <a href="#" @click="eventBus.emit('open:editBlogModal', blog)">{{blog.title}}</a>
                    </div>
                </div>
                <div class="mt-2 mb-2">
                    <input type="text" class="form-control" placeholder="Search..." v-model="searchText">
                </div>
                <CollapseDiv :elId="getNewElUid()" :isClosed="isMobile && !searchText">
                    <template v-slot:header>
                        Recent posts
                    </template>
                    <div v-for="blog in displayedBlogs" class="row mb-4">
                        <div class="col-3">
                            <img v-if="blog.picture" :src="blog.picture" alt="Blog image">
                        </div>
                        <div class="col-9">
                            <h6><a :href="`/blog/${blog.id}/`">{{blog.title}}</a></h6>
                        </div>
                    </div>
                    <Pagination
                        ref="blogsPagination"
                        :items="filteredBlogs"
                        :itemsPerPage="blogsPerPage"
                        class="ms-1"
                        @pageChange="blogPaginationIdx = ($event - 1) * blogsPerPage"
                    />
                </CollapseDiv>
            </div>
        </div>
    </BasePage>
    <EditBlogModal v-if="isSuperUser" newInitDataKey="blogs"/>
</template>

<script>
import BasePage from "../base/BasePage";
import CollapseDiv from "../../components/CollapseDiv";
import dataUtil from "../../../utils/data";
import EditBlogModal from "../../modals/EditBlogModal";
import Pagination from "../../components/Pagination";

export default {
    name: "BlogPage.vue",
    components: {BasePage, CollapseDiv, EditBlogModal, Pagination},
    data() {
        return {
            blogsPerPage: 5,
            blogPaginationIdx: 0,
            searchText: null
        }
    },
    computed: {
        unpublishedPosts() {
            return this.initData.blogs.filter((b) => !b.isPublished);
        },
        publishedPosts() {
            return this.sortByDate(this.initData.blogs.filter((b) => b.isPublished));
        },
        filteredBlogs() {
            const searchTextRE = (this.searchText) ? RegExp(`^.*?${this.searchText}.*?$`, 'i') : null;
            return this.publishedPosts.filter((b) => !searchTextRE || b.title.match(searchTextRE))
        },
        displayedBlogs() {
            return this.filteredBlogs.slice(this.blogPaginationIdx, this.blogPaginationIdx + this.blogsPerPage + 1);
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