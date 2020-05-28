const backToStore = document.querySelector('.back-store');
const signOutStore = document.querySelector('.logout');

function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
        console.log('User signed out.');
    });
}

backToStore.addEventListener('click', e => {
    e.preventDefault();
    window.location.href = "/store";
})

signOutStore.addEventListener('click', e => {
    e.preventDefault();
    signOut();
    deleteCookie("email");
    window.location.href = "/";
})