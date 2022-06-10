<template>
    <BasePage>
        <div class="row justify-content-center">
            <template v-for="project in initData.projects">
                <ProjectCard :cardItem="project"></ProjectCard>
            </template>
            <p v-if="!initData.projects.length" class="float-end" style="width: auto">No projects to display</p>
        </div>
    </BasePage>
</template>

<script>
import BasePage from "../base/BasePage";
import ProjectCard from "./ProjectCard";
import PageHeader from "../../components/PageHeader";
import BaseFilter from "../base/BaseFilter";

export default {
    name: "ProjectsPage.vue",
    components: {
        BaseFilter, BasePage, PageHeader, ProjectCard,
    },
}
</script>