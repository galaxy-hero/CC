const signOutStore = document.querySelector('.logout');
const backToChat = document.querySelector('.back-chat');
const laptops = document.querySelector('.laps');
const pcs = document.querySelector('.pcs');
const accs = document.querySelector('.accessories');
const soft = document.querySelector('.software');
const cours = document.querySelector('.courses');


function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
        console.log('User signed out.');
    });
}

signOutStore.addEventListener('click', e => {
    e.preventDefault();
    signOut();
    deleteCookie("email");
    window.location.href = "/";
})

backToChat.addEventListener('click', e => {
    e.preventDefault();
    window.location.href = "/chat";
})

laptops.addEventListener('click', e => {
    e.preventDefault();
    window.location.href = "/laptops";
})

pcs.addEventListener('click', e => {
    e.preventDefault();
    window.location.href = "/pcs";
})

accs.addEventListener('click', e => {
    e.preventDefault();
    window.location.href = "/accessories";
})

soft.addEventListener('click', e => {
    e.preventDefault();
    window.location.href = "/software";
})

cours.addEventListener('click', e => {
    e.preventDefault();
    window.location.href = "/courses";
})


