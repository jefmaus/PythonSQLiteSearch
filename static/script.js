document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('userInput').addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
            sendQuery();
        }
    });
});

function sendQuery() {
    const userInput = document.getElementById('userInput').value;
    if (!userInput) {
        alert('Por favor, ingresa una instrucción.');
        return;
    }

    addMessageToChat('user', userInput);

    fetch('/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            data.error="La pregunta del usuario no está relacionada con alguna incidencia en particular. Por favor reformula la pregunta con más detalles sobre la incidencia que te interesa." 
            addMessageToChat('response', data.error);
        } else {
            addMessageToChat('response', data.response);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

    document.getElementById('userInput').value = '';
}

function addMessageToChat(sender, message) {
    const chatContainer = document.getElementById('chatContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    messageDiv.innerHTML = `${sender === 'user' ? 'Tú: ' : 'Respuesta: '}${message}`;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function resetChat() {
    const chatContainer = document.getElementById('chatContainer');
    chatContainer.innerHTML = '';
}
