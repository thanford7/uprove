import globalData from "../../../globalData";
const CONTENT = {
    draftStatusInfo: `
        <p>When in <code>draft</code> status, project will be:</p>
        <ul class='fa-ul'>
            <li><span class='fa-li'><i class='fas fa-check-circle -color-green-text'></i></span>Visible in your dashboard</li>
            <li><span class='fa-li'><i class='fas fa-check-circle -color-green-text'></i></span>Visible in your profile if you have chosen to display it</li>
            <li><span class='fa-li'><i class='fas fa-times-circle -color-red-text'></i></span>Not visible in employer searches for this project</li>
            <li><span class='fa-li'><i class='fas fa-times-circle -color-red-text'></i></span>Not available to submit for any employer job applications</li>
        </ul>
    `,
    completeStatusInfo: `
        <p>When in <code>complete</code> status, project will be:</p>
        <ul class='fa-ul'>
            <li><span class='fa-li'><i class='fas fa-check-circle -color-green-text'></i></span>Visible in your dashboard</li>
            <li><span class='fa-li'><i class='fas fa-check-circle -color-green-text'></i></span>Visible in your profile if you have chosen to display it</li>
            <li><span class='fa-li'><i class='fas fa-check-circle -color-green-text'></i></span>Visible in employer searches for this project</li>
            <li><span class='fa-li'><i class='fas fa-check-circle -color-green-text'></i></span>Available to submit for any employer job applications</li>
        </ul>
        <p><i class="fas fa-exclamation-triangle -color-yellow-text"></i> Once you change to <code>complete</code> status, you will be unable 
        to change the project for ${globalData.PROJECT_COMPLETE_LOCK_DAYS} days to
        give employers time to review the project without any new changes.</p>
    `,
    hiddenStatusInfo: `
        <p>When in <code>hidden</code> status, project will be:</p>
        <ul class='fa-ul'>
            <li><span class='fa-li'><i class='fas fa-check-circle -color-green-text'></i></span>Visible in your dashboard</li>
            <li><span class='fa-li'><i class='fas fa-check-circle -color-green-text'></i></span>Visible in your profile if you have chosen to display it</li>
            <li><span class='fa-li'><i class='fas fa-times-circle -color-red-text'></i></span>Not visible in employer searches for this project</li>
            <li><span class='fa-li'><i class='fas fa-check-circle -color-green-text'></i></span>Available to submit for any employer job applications</li>
        </ul>
    `
}

export default CONTENT;