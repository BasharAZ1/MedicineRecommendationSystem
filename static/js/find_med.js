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
                            });
                    });
                    suggestionsDiv.appendChild(div);
                });
            });
    } else {
        document.getElementById('navbar-suggestions').innerHTML = '';
    }
});
