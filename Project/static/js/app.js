//DOM queries
const chatList = document.querySelector('.chat-list');
const translate = document.querySelector('.translate');
const newChatForm = document.querySelector('.new-chat');
const newNameForm = document.querySelector('.new-name');
const updateMsg = document.querySelector('.update-msg');
const rooms = document.querySelector('.chat-rooms');
const check = document.querySelector('.check');
const visitStore = document.querySelector('.visit-store');
const signOutStore = document.querySelector('.logout');


const email = readCookie('email');

function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
        console.log('User signed out.');
    });
}

signOutStore.addEventListener('click', e => {
    e.preventDefault();
    signOut();
    deleteCookie('email');
    window.location.href = "/";
})

//add new chat
newChatForm.addEventListener('submit', e => {
    e.preventDefault();
    const message = newChatForm.message.value.trim();
    chatroom.addChat(message)
        .then(() => newChatForm.reset())
        .catch(err => console.log(err));
});

//update username
newNameForm.addEventListener('submit', e => {
    e.preventDefault();
    const newName = newNameForm.name.value.trim();
    chatroom.updateName(newName);
    newNameForm.reset();

    //show then hide username update message
    updateMsg.innerText = `Your name is now ${newName}`;
    setTimeout(() => {
        updateMsg.innerText = ''
    }, 5000)
});


$('#show').on('click', function () {
    $('.center').show();
    $(this).hide();
});

$('#close').on('click', function () {
    $('.center').hide();
    $('#show').show();
});


//update chatroom
rooms.addEventListener('click', e => {
    if (e.target.tagName === 'BUTTON') {
        chatUI.clear();
        chatroom.updateRoom(e.target.getAttribute('id'));
        chatroom.getChats(chat => chatUI.render(chat));
    }
});

//translate button func
translate.addEventListener('click', e => {
    var data2 = document.getElementById('message').value;
    /*$.post('/translate', data, function(data, status){
        console.log(`${data} and status is ${status}`)
    }, 'json')*/
    jQuery.ajax({
        url: '/translate',
        type: "POST",
        data: JSON.stringify([{"Text": data2}]),
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (resp) {
            //console.log(data2);
            console.log(`${JSON.stringify(resp)} and status is ${status}`);
            console.log(resp[0].translations[0].text);
            document.getElementById('message').value = resp[0].translations[0].text;
        }
    });
});


check.addEventListener('click', e => {
    var data = document.getElementById('message').value;
    /*$.post('/translate', data, function(data, status){
        console.log(`${data} and status is ${status}`)
    }, 'json')*/
    jQuery.ajax({
        url: '/check',
        type: "POST",
        data: JSON.stringify({"text": data}),
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (resp) {
            if (resp["spell_checked"] !== "") {
                document.getElementById("message").value = resp["spell_checked"];
            }
        }
    });
})

visitStore.addEventListener('click', e => {
    e.preventDefault();
    window.location.href = "/store";
})


//check local storage for an existing name
const username = localStorage.username ? localStorage.username : 'anonymous';

//class instances
const chatUI = new ChatUI(chatList);
const chatroom = new Chatroom('java', username);
chatroom.updateEmail(email);

//get chats and render
chatroom.getChats((data) => {
    chatUI.render(data);
    const upvote = document.querySelector('.points-button');
    //give points
    upvote.addEventListener('click', e => {

        e.preventDefault();
        const pointsMsg = document.querySelector('.update-points-msg');
        pointsMsg.innerText = `You upvoted this response!`;
        setTimeout(() => {
            pointsMsg.innerText = ''
        }, 2000)
    })
});