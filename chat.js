const chatBox = document.getElementById("chat-box");
const input = document.getElementById("message");
const sendBtn = document.getElementById("sendBtn");

// Welcome message
addBotMessage("👋 Hello! I'm QueryBot. Ask me anything!");

sendBtn.addEventListener("click", sendMessage);

input.addEventListener("keypress", function(e){
    if(e.key === "Enter"){
        sendMessage();
    }
});

async function sendMessage(){

    const message = input.value.trim();

    if(message === "") return;

    addUserMessage(message);

    input.value="";

    const typing = document.createElement("div");

    typing.className="bot";

    typing.id="typing";

    typing.innerHTML="🤖 QueryBot is typing...";

    chatBox.appendChild(typing);

    scrollDown();

    try{

        const response = await fetch("/chat",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                message:message
            })

        });

        const data = await response.json();

        document.getElementById("typing").remove();

        addBotMessage(data.reply);

    }

    catch(error){

        document.getElementById("typing").remove();

        addBotMessage("❌ Something went wrong.");

        console.error(error);

    }

}

function addUserMessage(message){

    const div=document.createElement("div");

    div.className="user";

    div.innerHTML=message;

    chatBox.appendChild(div);

    scrollDown();

}

function addBotMessage(message){

    const div=document.createElement("div");

    div.className="bot";

    div.innerHTML=message;

    chatBox.appendChild(div);

    scrollDown();

}

function scrollDown(){

    chatBox.scrollTop=chatBox.scrollHeight;

}