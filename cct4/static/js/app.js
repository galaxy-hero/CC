
//DOM queries
const chatList = document.querySelector('.chat-list');
const translate = document.querySelector('.translate');
const newChatForm = document.querySelector('.new-chat');
const newNameForm = document.querySelector('.new-name');
const updateMsg = document.querySelector('.update-msg');
const rooms = document.querySelector('.chat-rooms');
const chatField = document.getElementById('message');


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

//update chatroom
rooms.addEventListener('click', e => {
    if(e.target.tagName === 'BUTTON'){
        chatUI.clear();
        chatroom.updateRoom(e.target.getAttribute('id'));
        chatroom.getChats(chat => chatUI.render(chat));
    }
});

//translate button func
data = [{"Text":"Hello, what is your name?"}];
translate.addEventListener('click', e => {
    console.log(data);
    var data2 = document.getElementById('message').value;
    /*$.post('/translate', data, function(data, status){
        console.log(`${data} and status is ${status}`)
    }, 'json')*/
    jQuery.ajax ({
        url: '/translate',
        type: "POST",
        data: JSON.stringify([{"Text":data2}]),
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function(resp){
            //console.log(data2);
            console.log(`${JSON.stringify(resp)} and status is ${status}`)
            console.log(resp[0].translations[0].text)
            document.getElementById('message').value = resp[0].translations[0].text;
        }
    });
})

//autosuggest
chatField.addEventListener('keyup', e => {
    console.log(e.target.value.trim());
    jQuery.ajax({
        type: "GET",
        url: `/autosuggest?text=${e.target.value.trim()}`,
        dataType: "text",
        contentType: "application/text; charset=utf-8",
        success: function(resp){
            //console.log(`${JSON.stringify(resp)} and status is ${status}`)
            //console.log(resp[0].translations[0].text)
            //document.getElementById('message').value = resp[0].translations[0].text;
        }
    })
})

//check local storage for an existing name
const username = localStorage.username ? localStorage.username : 'anonymous';

//class instances
const chatUI = new ChatUI(chatList);
const chatroom = new Chatroom('java', username);

//get chats and render
chatroom.getChats((data) => {
    chatUI.render(data);
});