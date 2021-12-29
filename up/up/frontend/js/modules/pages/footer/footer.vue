<template>
    <div class="pt-4 pb-2 ps-4 pe-4 container-lg">
        <div class="row align-items-center mb-2">
            <div v-for="(section, idx) in sections" :key="idx" class="col-md-3 col-12 mb-2">
                <ul class="list-table">
                    <li><span class="-text-bold">{{section.header}}</span></li>
                    <li v-for="(item, iIdx) in section.items" :key="iIdx">
                        <i v-if="item.icon" class="fab" :class="item.icon"></i>&nbsp;
                        <a :href="item.link" :target="(item.isNewTab) ? '_blank' : ''">
                            {{item.title}}
                        </a>
                    </li>
                </ul>
            </div>
            <div class="col-md-6 col-12 mb-2">
                <img class="logo" :class="(isMobile) ? '' : 'float-end'" :src="globalData.STATIC_URL + 'img/logo.png'" alt="Uprove" height="40" width="118">
            </div>
        </div>
        <div class="d-md-inline-block">&copy; {{(startYear !== currentYear) ? `${startYear}-` : ''}}{{currentYear}} Uprove, Inc.&nbsp;&nbsp;</div>
        <div class="d-md-inline-block"><a href="/terms-of-service">Terms of service</a>&nbsp;&nbsp;</div>
        <div class="d-md-inline-block"><a href="/privacy">Privacy policy</a></div>
    </div>
</template>
<script>
import dayjs from "dayjs/esm";

export default {
    data() {
        return {
            sections: [
                {
                    header: 'Company',
                    items: [
                        {
                            title: 'About us',
                            link: '/about'
                        },
                        {
                            title: 'Contact',
                            link: '/contact'
                        },
                        {
                            title: 'Blog',
                            link: '/blog'
                        }
                    ]
                },
                {
                    header: 'Connect',
                    items: [
                        {
                            icon: 'fa-twitter-square',
                            title: 'Follow us on Twitter',
                            link: 'https://twitter.com/uprove_co',
                            isNewTab: true
                        },
                        {
                            icon: 'fa-linkedin',
                            title: 'Connect on LinkedIn',
                            link: 'https://linkedin.com/company/uprove-co',
                            isNewTab: true
                        }
                    ]
                }
            ],
            currentYear: dayjs().year(),
            startYear: 2021
        }
    },
}
</script>