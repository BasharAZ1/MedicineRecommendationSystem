document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('#nav-links a');


    const usernameElement = document.getElementById('username');
    const hamburgerMenu = document.querySelector('.burger-menu');
    const sidebar = document.querySelector('.nav-links');
    
    hamburgerMenu.addEventListener('click', () => {
        sidebar.classList.toggle('active');
    });

    // fetch('/api/session')
    //     .then(response => {
    //         if (!response.ok) {
    //             throw new Error('Network response was not ok');
    //         }
    //         return response.json();
    //     })
    //     .then(data => {
    //         if (data.is_logged_in) {
    //             usernameElement.textContent = data.username;
    //         } else {
    //             window.location.href = 'login.html';
    //         }
    //     })
    //     .catch(error => console.error('Error fetching session data:', error));

    // Debounce function to limit the rate of API calls
    function debounce(func, delay) {
        let debounceTimer;
        return function() {
            const context = this;
            const args = arguments;
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => func.apply(context, args), delay);
        };
    }

    // Function to handle search input
    function handleSearchInput() {
        const query = document.getElementById('navbar-search').value;
        if (query.length > 1) {
            fetch(`/api/search?query=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    const suggestionsDiv = document.getElementById('navbar-suggestions');
                    suggestionsDiv.innerHTML = '';
                    data.suggestions.forEach(suggestion => {
                        const div = document.createElement('div');
                        div.className = 'suggestion';
                        div.innerText = suggestion.name;
                        div.addEventListener('click', () => {
                            document.getElementById('navbar-search').value = suggestion.name;
                            fetch(`/api/get_medicine_info?name=${encodeURIComponent(suggestion.name)}`)
                                .then(response => response.json())
                                .then(info => {
                                    const newWindow = window.open('', '_blank', 'width=400,height=400');
                                    if (newWindow) {
                                        newWindow.document.write(`
                                            <h2>${info.name}</h2>
                                            <p><strong>Chemical Class:</strong> ${info.chemical_class}</p>
                                            <p><strong>Habit Forming:</strong> ${info.habit_forming}</p>
                                            <p><strong>Therapeutic Class:</strong> ${info.therapeutic_class}</p>
                                            <p><strong>Action Class:</strong> ${info.action_class}</p>
                                            <p><strong>Side Effects:</strong> ${info.side_effects.join(', ')}</p>
                                            <p><strong>Uses:</strong> ${info.uses.join(', ')}</p>
                                            <p><strong>Substitute Drugs:</strong> ${info.substitutes.join(', ')}</p>
                                        `);
                                    }
                                });
                        });
                        suggestionsDiv.appendChild(div);
                    });
                })
                .catch(error => console.error('Error fetching suggestions:', error));
        } else {
            document.getElementById('navbar-suggestions').innerHTML = '';
        }
    }

    // Apply debounce to the search input handler
    document.getElementById('navbar-search').addEventListener('input', debounce(handleSearchInput, 300));

    document.getElementById('search-button').addEventListener('click', function() {
        const query = document.getElementById('navbar-search').value;
        if (query.length > 1) {
            fetch(`/api/FDA_search?query=${encodeURIComponent(query)}`)
                .then(response => {
                    if (response.status === 404) {
                        const newWindow = window.open('', '_blank', 'width=400,height=200');
                        if (newWindow) {
                            newWindow.document.write('<h2>Drug Information</h2><p>Not found</p>');
                        }
                        throw new Error('Not found');
                    }
                    return response.text();  // Changed from .json() to .text()
                })
                .then(responseText => {
                    let data;
                    try {
                        data = JSON.parse(responseText);
                    } catch (e) {
                        console.error('Error parsing JSON:', e);
                        console.error('Response text:', responseText);
                        alert('An error occurred while fetching the drug information.');
                        return;
                    }
                    if (data.error) {
                        alert(data.error);
                    } else {
                        const newWindow = window.open('', '_blank', 'width=400,height=600');
                        if (newWindow) {
                            newWindow.document.write(`
                                <h2>${data["Brand Name"]}</h2>
                                <p><strong>Generic Name:</strong> ${data["Generic Name"]}</p>
                                <p><strong>Manufacturer:</strong> ${data["Manufacturer"]}</p>
                                <p><strong>Active Ingredients:</strong> ${data["Active Ingredients"].join(', ')}</p>
                                <p><strong>Purpose:</strong> ${data["Purpose"].join(', ')}</p>
                                <p><strong>Indications and Usage:</strong> ${data["Indications and Usage"].join(', ')}</p>
                                <p><strong>Warnings:</strong> ${data["Warnings"].join(', ')}</p>
                                <p><strong>Dosage and Administration:</strong> ${data["Dosage and Administration"].join(', ')}</p>
                                <p><strong>Inactive Ingredients:</strong> ${data["Inactive Ingredients"].join(', ')}</p>
                            `);
                        }
                    }
                })
        }
    });

    // Handle logout
    document.getElementById('logout').addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the default link behavior
        fetch('/api/logout', {
            method: 'POST'
        })
        .then(response => {
            if (response.ok) {
                window.location.href = '/login';
            } else {
                console.error('Logout failed:', response.statusText);
                alert('Logout failed.');
            }
        })
        .catch(error => console.error('Error during logout:', error));
    });
});
