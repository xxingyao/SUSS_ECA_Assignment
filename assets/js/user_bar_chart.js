var ctx = document.getElementById('userChart').getContext('2d');

$.ajax({
    url: "/user_bar_chart",
    type: "POST",
    data: {},
    error: function() {
        alert("Error");
    },
    success: function(data) {
        var labels = data.labels;
        var cancelled = data.cancelled;
        var completed = data.completed;
        var upcoming = data.upcoming;

        const colors = {
            cancelled: '#36A2EB',   
            completed: '#FF6384',  
            upcoming: '#FFCE56' 
        };

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Cancelled',
                        backgroundColor: colors.cancelled,
                        data: cancelled
                    },
                    {
                        label: 'Completed',
                        backgroundColor: colors.completed,
                        data: completed
                    },
                    {
                        label: 'Upcoming',
                        backgroundColor: colors.upcoming,
                        data: upcoming
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            font: {
                                size: 12
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        stacked: false,
                        title: {
                            display: false
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: false
                        }
                    }
                }
            }
        });
    }
});