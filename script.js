AWS.config.region = "us-east-1";
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
  IdentityPoolId: "us-east-1:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", 
});

const lexruntime = new AWS.LexRuntimeV2();
const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const typingIndicator = document.getElementById("typing");

// helper to add messages
function addMessage(msg, sender) {
  const wrapper = document.createElement("div");
  wrapper.classList.add("flex", sender === "user" ? "justify-end" : "justify-start");
  const bubble = document.createElement("div");
  bubble.classList.add("rounded-2xl", "px-4", "py-2", "max-w-[75%]", "transition-all", "duration-300");
  if (sender === "user") {
    bubble.classList.add("bg-blue-600", "text-white");
  } else {
    bubble.classList.add("bg-blue-100", "text-gray-800");
  }
  bubble.textContent = msg;
  wrapper.appendChild(bubble);
  chatBox.appendChild(wrapper);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// typing indicator toggle
function showTypingIndicator(show) {
  typingIndicator.classList.toggle("hidden", !show);
}

// send message to Lex
function sendMessage() {
  const message = input.value.trim();
  if (!message) return;
  addMessage(message, "user");
  input.value = "";
  showTypingIndicator(true);

  const params = {
    botId: "YOUR_BOT_ID",
    botAliasId: "YOUR_BOT_ALIAS_ID",
    localeId: "en_US",
    sessionId: "web-" + Date.now(),
    text: message
  };

  lexruntime.recognizeText(params, (err, data) => {
    showTypingIndicator(false);
    if (err) {
      console.error(err);
      addMessage(" Error connecting to bot. Check console for details.", "bot");
    } else {
      const reply = data.messages && data.messages[0] ? data.messages[0].content : "🤖 (no response)";
      addMessage(reply, "bot");
    }
  });
}

sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keypress", (e) => { if (e.key === "Enter") sendMessage(); });

// simple animated dots for typing indicator
setInterval(() => {
  const dots = document.querySelector("#typing .dots");
  if (dots) {
    dots.textContent = dots.textContent.length >= 3 ? "." : dots.textContent + ".";
  }
}, 400);
