<template>
    <BasePage>
        <div class="row">
            <div v-for="course in initData.courses" class="col-md-4 card-course">
                <div class="card-course__cover">
                    <img :src="course.coverImage" alt="Course">
                </div>
                <div class="card-course__price">
                    {{ (course.priceBasic) ? `$${course.priceBasic}` : 'FREE' }}
                </div>
                <div class="card-course__description">
                    {{ course.shortDescription }}
                    &nbsp;
                    <a :href="getSalesPageUrl(course.salesPageSlug)" target="_blank">
                        Learn more <i class="fas fa-external-link-alt"></i>
                    </a>
                </div>

            </div>
        </div>
    </BasePage>
</template>

<script>
import BasePage from "../base/BasePage";
export default {
    name: "CoursesPage",
    components: {BasePage},
    data() {
        return {
            baseTeachableUrl: 'https://training.uprove.co/'
        }
    },
    methods: {
        getSalesPageUrl(slug) {
            return `${this.baseTeachableUrl}p/${slug}`
        }
    }
}
</script>