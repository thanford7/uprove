<template>
    <div class="container-lg">
        <BannerAlert/>
        <slot name="header">
            <PageHeader :title="headerTitle" :image="headerImage" :imageAlt="headerImageAlt"/>
        </slot>
        <div class="row filter mb-3">
            <slot name="filter"></slot>
        </div>
        <slot></slot>
    </div>
</template>

<script>
import BannerAlert from "../components/BannerAlert";
import PageHeader from "../components/PageHeader";

export default {
    name: "BasePage",
    props: ['headerTitle', 'headerImage', 'headerImageAlt'],
    components: {BannerAlert, PageHeader}
}
</script>