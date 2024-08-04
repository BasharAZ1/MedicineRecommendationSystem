// Determine the current path
const currentPath = window.location.pathname;
const authPages = ['/login', '/signup'];
const isAuthPage = authPages.includes(currentPath);
const usernameElement = document.getElementById('username');
// Fetch login status from the server
fetch('/api/session')
    .then(response => response.json())
    .then(data => {
        if (data.is_logged_in) {
            usernameElement.textContent = data.username;
            if (isAuthPage) {

                window.location.href = '/index';  // Replace with your index page URL
            }
        } else {
            // Redirect to login page if not logged in and on an auth page
            if (!isAuthPage) {
                window.location.href = '/login';  // Replace with the login page URL
            }
        }
    })
    .catch(error => {
        console.error('Error checking login status:', error);
        // Optionally handle the error, e.g., show a message to the user
    });