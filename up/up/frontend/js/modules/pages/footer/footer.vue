<template>
    <div class="pt-4 pb-2 ps-4 pe-4">
        <div class="row algin-items-center mb-2">
            <div v-for="(section, idx) in sections" :key="idx" class="col-md-3 col-12 mb-2">
                <ul class="list-table">
                    <li><span class="-text-bold">{{section.header}}</span></li>
                    <li v-for="(item, iIdx) in section.items" :key="iIdx">
                        <font-awesome-icon v-if="item.icon" :icon="item.icon"/>&nbsp;
                        <a :href="item.link">
                            {{item.title}}
                        </a>
                    </li>
                </ul>
            </div>
            <div v-if="!isProfile" class="col-md-6 col-12">
                <span class="-text-bold">Get started</span>
                <div class="row mb-2">
                    <div class="col-3">
                        <label for="employerEmail" class="col-form-label">Employers</label>
                    </div>
                    <div class="col-9">
                        <div class="input-group input-group-sm">
                            <input type="email" class="form-control" id="employerEmail" placeholder="Email...">
                            <span class="input-group-text -color-orange" @click="sendEmail">
                                <font-awesome-icon :icon="['fas', 'paper-plane']"/>&nbsp;
                                Request demo&nbsp;&nbsp;&nbsp;&nbsp;
                            </span>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-3 ">
                        <label for="seekerEmail" class="col-form-label">Job seekers</label>
                    </div>
                    <div class="col-9">
                        <div class="input-group input-group-sm">
                            <input type="email" class="form-control" id="seekerEmail" placeholder="Email...">
                            <span class="input-group-text -color-orange" @click="sendEmail">
                                <font-awesome-icon :icon="['fas', 'paper-plane']"/>&nbsp;
                                Request account
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="d-md-inline-block">&copy; {{currentYear}} Uprove, Inc.&nbsp;&nbsp;</div>
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
                            link: 'about'
                        },
                        {
                            title: 'Contact',
                            link: 'contact'
                        }
                        // {
                        //     title: 'Blog',
                        //     link: ''
                        // }
                    ]
                },
                {
                    header: 'Connect',
                    items: [
                        {
                            icon: ['fab', 'twitter-square'],
                            title: 'Follow us on Twitter',
                            link: 'https://twitter.com/uprove_co'
                        },
                        {
                            icon: ['fab', 'linkedin'],
                            title: 'Connect on LinkedIn',
                            link: 'https://linkedin.com/company/uprove-co'
                        }
                    ]
                }
            ],
            currentYear: dayjs().year()
        }
    },
    props: ['isProfile'],
    methods: {
        sendEmail() {
            //
        }
    }
}
</script>