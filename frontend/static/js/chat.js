async function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (!userInput.trim()) return;

    // Append user message to chatbox
    appendMessage('You', userInput);

    const response = await fetch('chat_service/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt: userInput })
    });

    const data = await response.json();
    appendMessage('Assistant', data.response);

    // Clear the input field
    document.getElementById('user-input').value = '';
}

async function resetChat() {
    await fetch('chat_service/reset', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    });

    document.getElementById('chatbox').innerHTML = '';
}

function appendMessage(sender, message) {
    const chatbox = document.getElementById('chatbox');
    const messageElement = document.createElement('div');
    messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatbox.appendChild(messageElement);
    chatbox.scrollTop = chatbox.scrollHeight;
}
