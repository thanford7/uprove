<template>
    <div>
        <div class="courses-background">
            <div class="container-fluid">
                <div class="row">
                    <div class="col-md-6 p-3 d-flex align-items-center">
                        <h4 class="text-center">Live And On-Demand Customer Success Courses</h4>
                    </div>
                    <div class="col-md-6 p-3 -color-white -color-darkblue-text">
                        <h5 class="text-center">Your skills from completed courses are showcased on your Uprove profile and searchable by employers looking to hire</h5>
                        <img :src="globalData.STATIC_URL + 'img/uproveCertifications.png'" alt="Uprove credentials">
                    </div>
                </div>
            </div>
        </div>
        <BasePage>
            <div class="row">
                <div v-for="course in initData.courses" class="col-md-4 mb-3" :set="userCourse = getUserCourse(course)">
                    <div class="card-course">
                        <div class="card-course__cover">
                            <img :src="course.coverImage" alt="Course">
                        </div>
                        <div v-if="!userCourse" class="card-course__price">
                            {{ (course.priceBasic) ? `$${course.priceBasic}` : 'FREE' }}
                        </div>
                        <div class="card-course__description">
                            {{ course.shortDescription }}
                            &nbsp;
                            <a v-if="!userCourse" :href="getSalesPageUrl(course.salesPageSlug)" target="_blank">
                                Learn more <i class="fas fa-external-link-alt"></i>
                            </a>

                            <div v-if="userCourse" class="mt-2">
                                <span class="-text-bold">Course progress</span>
                                <ProgressPill :pctComplete="userCourse.completionPct" color="darkblue" :text="`${userCourse.completionPct}%`"/>
                                <div class="mt-2">
                                    <a class="btn btn-primary btn-sm w-100" :href="getCoursePageUrl(course)" target="_blank">
                                        {{ (userCourse.completedDateTime) ? 'Review' : 'Continue' }}
                                        course <i class="fas fa-external-link-alt"></i>
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </BasePage>
    </div>
</template>

<script>
import BasePage from "../base/BasePage";
import ProgressPill from "../../components/ProgressPill";
export default {
    name: "CoursesPage",
    components: {ProgressPill, BasePage},
    data() {
        return {
            baseTeachableUrl: 'https://training.uprove.co/'
        }
    },
    methods: {
        getCoursePageUrl(course) {
            return `${this.baseTeachableUrl}courses/enrolled/${course.teachableCourseId}`;
        },
        getSalesPageUrl(slug) {
            return `${this.baseTeachableUrl}p/${slug}`;
        },
        getUserCourse(course) {
            if (!this.initData.user || !this.initData.user.courses.length) {
                return null;
            }
            return this.initData.user.courses.find((c) => c.courseId === course.id);
        }
    }
}
</script>