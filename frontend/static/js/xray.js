document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('fileInput');
    const imageDisplay = document.getElementById('imageDisplay');
    const predictButton = document.getElementById('predictButton');
    const fetchTablesButton = document.getElementById('fetchTablesButton');
    const predictionResult = document.getElementById('predictionResult');
    const tablesResult = document.getElementById('tablesResult');
    const submitFeedbackButton = document.getElementById('submitFeedbackButton');
    const feedbackLabel = document.getElementById('feedbackLabel');
    const feedbackText = document.getElementById('feedbackText');
    let selectedFile;
    let selectedFileName;

    // Fetch and populate labels
    function populateLabels() {
        const keyword = document.getElementById('h1Content').textContent.split(' ')[0];
        const url = `/api/${encodeURIComponent(keyword)}-get-labels`;
    
        fetch(url)
            .then(response => response.json())
            .then(data => {
                feedbackLabel.innerHTML = '';
                data.labels.forEach(label => {
                    const option = document.createElement('option');
                    option.value = label;
                    option.textContent = label;
                    feedbackLabel.appendChild(option);
                });
            })
            .catch(error => {
                console.error('Error fetching labels:', error);
                alert('An error occurred while fetching labels. Please try again.');
            });
    }
    
    // Call populateLabels on page load
    populateLabels();

    fileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            selectedFileName = file.name;
            const reader = new FileReader();
            reader.onload = (e) => {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.style.width = '100%';
                img.style.height = 'auto';
                imageDisplay.innerHTML = '';
                imageDisplay.appendChild(img);
            }
            reader.readAsDataURL(file);
            selectedFile = file;
        }
    });

    predictButton.addEventListener('click', () => {
        if (selectedFile) {
            const formData = new FormData();
            formData.append('file', selectedFile);
            const keyword = document.getElementById('h1Content').textContent.split(' ')[0];

            const url = `/api/${encodeURIComponent(keyword)}`;

            fetch(url, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                predictionResult.innerText = 'Prediction: ' + data.prediction;
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            });
        } else {
            alert('Please upload an image first.');
        }
    });


    submitFeedbackButton.addEventListener('click', () => {
        if (!selectedFileName) {
            alert('Please upload an image first.');
            return;
        }

        const feedback = {
            pictureName: selectedFileName,
            label: feedbackLabel.value,
            comments: feedbackText.value,
            prediction: predictionResult.innerText
        };

        fetch('/api/submitfeedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(feedback)
        })
        .then(response => response.json())
        .then(data => {
            alert('Feedback submitted successfully');
            feedbackText.value = '';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while submitting feedback. Please try again.');
        });
    });

    // Populate labels on page load
    populateLabels();
});
