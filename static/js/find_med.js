
    document.getElementById('burger-menu').addEventListener('click', function() {
        document.getElementById('nav-links').classList.toggle('active');
    });

    document.getElementById('search-button').addEventListener('click', function() {
        const query = document.getElementById('navbar-search').value;
        if (query.length > 1) {
            fetch(`/FDA_search?query=${query}`)
                .then(response => {
                    if (response.status === 404) {
                        const newWindow = window.open('', '_blank', 'width=400,height=200');
                        if (newWindow) {
                            newWindow.document.write('<h2>Drug Information</h2><p>Not found</p>');
                        } 
                    }
                    return response.json();
                })
                .then(data => {
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
                .catch(error => {
                    if (error.message !== 'Not found') {
                        console.error('Error:', error);
                        alert('An error occurred while fetching the drug information.');
                    }
                });
        } else {
            alert('Please enter a valid search query.');
        }
    });

    document.getElementById('navbar-search').addEventListener('input', function() {
        const query = this.value;
        if (query.length > 1) {
            fetch(`/search?query=${query}`)
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
                            fetch(`/get_medicine_info?name=${encodeURIComponent(suggestion.name)}`)
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
                });
        } else {
            document.getElementById('navbar-suggestions').innerHTML = '';
        }
    });

