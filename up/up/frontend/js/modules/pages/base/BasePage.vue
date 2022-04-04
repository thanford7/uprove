<template>
    <div class="container-lg">
        <BannerAlert/>
        <slot name="header">
            <PageHeader v-if="headerTitle" :title="headerTitle" :image="headerImage" :imageAlt="headerImageAlt"/>
        </slot>
        <slot name="filter"></slot>
        <div class="mt-3">
            <slot></slot>
        </div>
    </div>
</template>

<script>
import BannerAlert from "../../components/BannerAlert";
import PageHeader from "../../components/PageHeader";

export default {
    name: "BasePage",
    props: ['headerTitle', 'headerImage', 'headerImageAlt'],
    components: {BannerAlert, PageHeader}
}
</script>