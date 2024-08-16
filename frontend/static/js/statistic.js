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
                        backgroundColor: 'rgba(255, 99, 132, 0.2)', // Change to a different color
                        borderColor: 'rgba(255, 99, 132, 1)', // Change to a different color
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
