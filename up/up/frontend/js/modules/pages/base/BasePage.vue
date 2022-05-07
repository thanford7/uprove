<template>
    <div class="ms-md-5 ms-2 me-md-5 me-2">
        <div class="container-fluid">
            <BannerAlert/>
            <slot name="header">
                <PageHeader v-if="headerTitle" :title="headerTitle" :image="headerImage" :imageAlt="headerImageAlt"/>
            </slot>
            <slot name="filter"></slot>
            <div class="mt-3">
                <slot></slot>
            </div>
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