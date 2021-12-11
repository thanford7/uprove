<template>
    <div id="home-page">
        <div class="row justify-content-center">
            <div class="col-md-8 mt-5 mb-4">
                <h2 class="text-center">
                    <strong>
                        Adding Uprove to your hiring process can reduce the frequency of bad hires by <span class="-color-orange-text">80%</span>
                    </strong>
                </h2>
            </div>
        </div>
        <div class="pt-3 pb-1 -border-top--light -border-bottom--light">
            <div class="row mb-2">
                <h1>Hiring made easy</h1>
            </div>
            <template v-if="!isMobile">
                <div class="row skewer-container skewer-container-hz justify-content-between">
                    <div v-for="num in [...Array(4).keys()]" class="circle emphasize" :data-em-key="num + 1">{{num + 1}}</div>
                    <div class="triangle__right" style="margin-right: -3px;"></div>
                    <div class="skewer"></div>
                </div>
                <div class="row mt-2">
                    <div class="col-md-3 p-2 emphasize" data-em-key="1">
                        <p>Find top-performing candidates with relevant skills by using Uprove's search engine <strong>or</strong>
                        direct your existing candidates to the Uprove platform</p>
                    </div>
                    <div class="col-md-3 p-2 emphasize" data-em-key="2">
                        <p>Candidates complete customized exercises that assess their talent in specific areas your hiring hiring for</p>
                    </div>
                    <div class="col-md-3 p-2 emphasize" data-em-key="3">
                        <p>Review submitted projects on your own time and select top candidates for further vetting</p>
                    </div>
                    <div class="col-md-3 p-2 emphasize" data-em-key="4">
                        <p>Hire better candidates in less time, and save money!</p>
                    </div>
                </div>
            </template>
            <template v-if="isMobile">
                <div class="row emphasize">
                    <div class="col-12" data-em-key="1">
                        <div class="circle d-inline-block -vertical-align-top">1</div>
                        <p class="d-inline-block w-75 ms-3">Find top-performing candidates with relevant skills by using Uprove's search engine <strong>or</strong>
                        direct your existing candidates to the Uprove platform</p>
                    </div>
                    <div class="col-12" data-em-key="2">
                        <div class="circle d-inline-block -vertical-align-top">2</div>
                        <p class="d-inline-block w-75 ms-3">Candidates complete customized exercises that assess their talent in specific areas your hiring hiring for</p>
                    </div>
                    <div class="col-12" data-em-key="3">
                        <div class="circle d-inline-block -vertical-align-top">3</div>
                        <p class="d-inline-block w-75 ms-3">Review submitted projects on your own time and select top candidates for further vetting</p>
                    </div>
                    <div class="col-12" data-em-key="4">
                        <div class="circle d-inline-block -vertical-align-top">4</div>
                        <p class="d-inline-block w-75 ms-3">Hire better candidates in less time, and save money!</p>
                    </div>
                </div>
            </template>
        </div>
        <div class="row justify-content-center -border-bottom--light">
            <div class="col-md-8 mt-4 mb-4">
                <h2 class="text-center">
                    <strong>
                        Uprove users can expect to save <span class="-color-orange-text">$7,500</span> per hire against standard recruiting practices
                    </strong>
                </h2>
            </div>
        </div>
        <div class="row mt-4 mb-4 pb-4 -border-bottom--light">
            <div class="col-md-7">
                <h2 class="text-center">
                    Uprove projects are built to assess the true talent of a candidate
                </h2>
                <img :src="globalData.STATIC_URL + 'img/projectChartExample.png'" alt="">
            </div>
            <div class="col-md-5 justify-content-center" style="flex-direction: column; display: flex;">
                <div class="mb-3">
                    <h3 id="roles-rotation">Uprove has customized exercises for:</h3>
                </div>
                <div>
                    <h3 id="skills-rotation">Across a variety of tools and skills:</h3>
                </div>
            </div>
        </div>
        <div class="row mt-4 mb-4 pb-4 -border-bottom--light">
            <div class="col-md-4 justify-content-center" style="flex-direction: column; display: flex;">
                <h1>Uprove helps non-traditional candidates display their talent and find jobs they are qualified for.</h1>
                <p class="-color-moderategrey-text">
                    There are over 70 million Americans who are STARs...or “skilled through alternative routes”.
                    Many hiring processes automatically filter out these candidates due to their non-traditional
                    background. Uprove gives all candidates a channel to display their talent and find
                    fulfilling employment.
                </p>
            </div>
            <div class="col-md-8">
                <img :src="globalData.STATIC_URL + 'img/happyCandidates.jpg'" alt="">
            </div>
        </div>
        <div class="row mt-4 mb-4 pb-4">
            <h2><strong>Uprove was started after the founders saw the benefits and positive impact project interviews had
            on their hiring process.
            </strong></h2>
            <div><a href="/about/">Learn more about Uprove's origin and mission</a></div>
        </div>
        <EmployerRequestInfoModal/>
        <CandidateRequestAccountModal/>
    </div>
</template>
<script>
import CandidateRequestAccountModal from "../../modals/CandidateRequestAccountModal";
import EmployerRequestInfoModal from "../../modals/EmployerRequestInfoModal";
import OrderedList from '../../components/OrderedList.vue';

export default {
    components: {
        CandidateRequestAccountModal, EmployerRequestInfoModal, OrderedList
    },
    mounted() {
        this.eventBus.on('ajaxSuccess', () => {
            this.alerts.push({
                message: 'Email sent successfully',
                alertType: 'success'
            });
        });
        this.eventBus.on('ajaxFailure', ({xhr, textStatus, errorThrown}) => {
            this.alerts.push({
                message: `Failed: ${xhr.responseText || errorThrown}`,
                alertType: 'danger'
            });
        });

        $('#home-page').on('mouseenter mouseleave', '.emphasize', (e) => {
            const emKey = $(e.currentTarget).data('em-key');
            const turnOn = e.type === 'mouseenter';
            $(`[data-em-key="${emKey}"]`).each((idx, domEl) => {
                const domEl$ = $(domEl);
                if (domEl$.hasClass('circle')) {
                    domEl$.toggleClass('circle-inverse', turnOn);
                } else {
                    domEl$.toggleClass('-text-bold', turnOn);
                }
            });
        });
    }
}
</script>