<template>
    <div id="home-page">
        <div class="container-lg">
            <div class="row justify-content-center">
                <div class="col-md-8 mt-5 mb-4">
                    <h2 class="text-center">
                        <strong>
                            Adding Uprove to your hiring process can reduce the frequency of bad hires by <span class="-color-orange-text">80%</span>
                        </strong>
                    </h2>
                </div>
            </div>
        </div>
        <div class="container-fluid pt-3 pb-1 ps-md-5 pe-md-5 -color-yellow__light">
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
                        <p>Candidates complete customized exercises that assess their talent in specific areas you're hiring for</p>
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
        <div class="container-lg">
            <div class="row justify-content-center">
                <div class="col-md-8 mt-5 mb-4">
                    <h2 class="text-center">
                        <strong>
                            Uprove users can expect to save <span class="-color-orange-text">$7,500</span> per hire against standard recruiting practices
                        </strong>
                    </h2>
                </div>
            </div>
        </div>
        <div class="container-fluid -color-darkblue__light">
            <div class="row mt-4 mb-4 pb-4 pt-4">
                <div class="col-md-7">
                    <h2 class="text-center">
                        Uprove projects are built to assess the true talent of a candidate
                    </h2>
                    <img :src="globalData.STATIC_URL + 'img/projectChartExample.png'" alt="" class="p-5">
                </div>
                <div class="col-md-5 justify-content-center" style="flex-direction: column; display: flex;">
                    <div class="mb-3">
                        <h3 id="roles-rotation">Uprove has customized projects for:</h3>
                    </div>
                    <div>
                        <h3 id="skills-rotation">Across a variety of tools and skills:</h3>
                    </div>
                    <div class="mt-4">
                        <button type="button" class="btn btn-lg btn-primary -color-darkblue" @click="openProjectsPage">
                            View projects <i class="fas fa-external-link-alt"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <div class="container-lg">
            <div class="row mb-2">
                <h1>How it works</h1>
            </div>
            <div class="row">
                <div class="col-md-3 mb-3 text-center">
                    <h4 class="mb-3">You are looking for a...</h4>
                    <div class="text-center" style="display: inline-block">
                        <i class="fas fa-user-tie fa-4x -color-blue-text"></i>
                        <div class="-sub-text">Product manager</div>
                    </div>
                </div>
                <div class="col-md-3 mb-3 text-center">
                    <h4 class="mb-3">Who is proficient in...</h4>
                    <div class="mb-2">
                        <div class="text-center" style="display: inline-block">
                            <i class="far fa-file-powerpoint fa-4x -color-blue-text"></i>
                            <div class="-sub-text">Powerpoint</div>
                        </div>
                    </div>
                    <div class="mb-2">
                        <div class="text-center" style="display: inline-block">
                            <i class="fas fa-laptop-code fa-4x -color-blue-text"></i>
                            <div class="-sub-text">Wireframing</div>
                        </div>
                    </div>
                    <div>
                        <div class="text-center" style="display: inline-block">
                            <i class="fas fa-chalkboard-teacher fa-4x -color-blue-text"></i>
                            <div class="-sub-text">Public speaking</div>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 mb-3 text-center">
                    <h4 class="mb-3">And has...</h4>
                    <div>
                        <div class="text-center" style="display: inline-block">
                            <i class="fas fa-user-ninja fa-4x -color-blue-text"></i>
                            <div class="-sub-text">Advanced experience (5+ years)</div>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 mb-3 text-center">
                    <h4 class="mb-3">Uprove provides...</h4>
                    <div class="mb-3">
                        <div class="text-center" style="display: inline-block">
                            <i class="fas fa-users fa-4x -color-orange-text"></i>
                            <div class="-sub-text">Top performing candidates who have completed projects that match your criteria</div>
                        </div>
                    </div>
                    <div>
                        <div class="text-center" style="display: inline-block">
                            <i class="fas fa-tasks fa-4x -color-orange-text"></i>
                            <div class="-sub-text">Projects that can be facilitated and evaluated through Uprove which assess candidates for your selected skills</div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="mt-4" :class="(isMobile) ? 'text-center' : ''">
                    <button type="button" class="btn btn-lg btn-primary -color-darkblue" @click="eventBus.emit('open:employerRequestInfoModal')">
                        Request demo
                    </button>
                </div>
            </div>
        </div>
        <div class="container-fluid -color-yellow__light">
            <div class="row mt-4 mb-4 pb-4 ps-4 pe-4 pt-4">
                <div class="col-md-6 justify-content-center" style="flex-direction: column; display: flex;">
                    <h1>Uprove helps non-traditional candidates display their talent and find jobs they are qualified for.</h1>
                    <p class="-color-moderategrey-text">
                        There are over 70 million Americans who are STARs...or “skilled through alternative routes”.
                        Many hiring processes automatically filter out these candidates due to their non-traditional
                        background. Uprove gives all candidates a channel to display their talent and find
                        fulfilling employment.
                    </p>
                </div>
                <div class="col-md-6">
                    <img :src="globalData.STATIC_URL + 'img/happyCandidates.jpg'" alt="" class="p-md-5 w-100">
                </div>
            </div>
        </div>
        <div class="container-lg">
            <div class="row mt-4 mb-4 pb-4">
                <h2><strong>Uprove was started after the founders saw the benefits and positive impact project interviews had
                on their hiring process.
                </strong></h2>
                <div><a href="/about/">Learn more about Uprove's origin and mission</a></div>
            </div>
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
    methods: {
        openProjectsPage() {
            window.open('/projects/', '_blank').focus();
        }
    },
    mounted() {
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