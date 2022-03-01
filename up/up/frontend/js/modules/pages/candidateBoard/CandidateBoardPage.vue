<template>
    <div class="container-lg">
        <BannerAlert/>
        <PageHeader title="Candidate Board"/>
        <div class="row mb-3">
            <div class="card-custom">
                <Table :data="initData.profiles" :headers="headers" emptyDataMessage="No current profiles">
                    <template v-slot:body>
                        <tr v-for="profile in initData.profiles">
                            <td>{{profile.firstName}}</td>
                            <td>{{profile.lastName}}</td>
                            <td><a :href="`/profile/${profile.profileId}/`">{{profile.profileName}}</a></td>
                        </tr>
                    </template>
                </Table>
            </div>
        </div>
    </div>
</template>

<script>
import BannerAlert from "../../components/BannerAlert";
import PageHeader from "../../components/PageHeader";
import Table from "../../components/Table";

export default {
    name: "CandidateBoardPage",
    components: {BannerAlert, PageHeader, Table},
    data() {
        return {
            headers: [[{'value': 'First name'}, {'value': 'Last name'}, {'value': 'Profile name'}]]
        }
    }
}
</script>