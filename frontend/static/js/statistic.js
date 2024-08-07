document.addEventListener('DOMContentLoaded', (event) => {
    fetchDataAndRenderChart();
});

function fetchDataAndRenderChart() {
    fetch('/api/drugs_data_fetch')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('myChart').getContext('2d');
            const labels = Object.keys(data);
            const values = Object.values(data);
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: '# of Searches',
                        data: values,
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        });
}
