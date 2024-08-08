document.addEventListener('DOMContentLoaded', function() {
    setTimeout(hideFlashMessages, 3000);

    document.querySelectorAll('form').forEach(function(form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const formType = form.getAttribute('data-form-type');
            const username = form.querySelector('input[name="username"]').value;
            const password = form.querySelector('input[name="password"]').value;
            let requestBody = { username, password };
            let apiUrl = '';

            if (formType === 'register') {
                const confirmPassword = form.querySelector('input[name="confirm_password"]').value;
                requestBody.confirm_password = confirmPassword;
                apiUrl = '/api/register';
            } else if (formType === 'login') {
                apiUrl = '/api/login';
            }

            fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestBody)
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    window.location.href = formType === 'register' ? 'login' : '/index';
                } else {
                    displayFlashMessage(data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                displayFlashMessage('An error occurred. Please try again.');
            });
        });
    });

    function hideFlashMessages() {
        let messages = document.querySelector('.flash-messages');
        if (messages) {
            messages.style.transition = 'opacity 0.5s ease';
            messages.style.opacity = '0';
            setTimeout(function() {
                messages.remove();
            }, 500);
        }
    }

    function displayFlashMessage(message) {
        const flashMessagesContainer = document.createElement('div');
        flashMessagesContainer.classList.add('flash-messages');
        const alert = document.createElement('div');
        alert.classList.add('alert');
        alert.textContent = message;
        flashMessagesContainer.appendChild(alert);
        document.querySelector('.login-container').appendChild(flashMessagesContainer);

        setTimeout(hideFlashMessages, 3000);
    }
});
