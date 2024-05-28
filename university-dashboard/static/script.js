document.addEventListener('DOMContentLoaded', function () {
    const allSideMenu = document.querySelectorAll('#sidebar .side-menu.top li a');

    allSideMenu.forEach(item => {
        const li = item.parentElement;

        item.addEventListener('click', function (e) {
            e.preventDefault(); // Prevent default link behavior

            allSideMenu.forEach(i => {
                i.parentElement.classList.remove('active');
            });
            li.classList.add('active');
        });
    });

    const menuBar = document.querySelector('#content nav .bx.bx-menu');
    const sidebar = document.getElementById('sidebar');

    menuBar.addEventListener('click', function () {
        sidebar.classList.toggle('hide');
    });

    const switchMode = document.getElementById('switch-mode');
    
    // Check if a user preference for dark mode exists in local storage
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    
    // Set initial dark mode state based on the stored preference or the default (light mode)
    document.body.classList.toggle('dark', isDarkMode);
    switchMode.checked = isDarkMode;

    switchMode.addEventListener('change', function () {
        if (this.checked) {
            document.body.classList.add('dark');
            localStorage.setItem('darkMode', 'true'); // Save dark mode preference
        } else {
            document.body.classList.remove('dark');
            localStorage.setItem('darkMode', 'false'); // Save light mode preference
        }
    });

    // Load data after setting up event listeners
    loadData();
});

  function loadData() {
    fetch('/api/dashboard_data')
        .then(response => response.json())
        .then(data => {
            const yearData = data.year_data;
            const genderData = data.gender_data;
            const specialtyData = data.specialty_data;
            

            // Populate data for the bar chart
            populateBarChart(yearData);

            // Populate data for the pie chart
            populatePieChart(genderData);

            // Populate data for the doughnut chart
            populateLineChart(specialtyData);

            // Additional function to load total students count if available
            loadTotals();
        });

// Fetch data from the API endpoint
fetch('/api/dashboard_data2')
    .then(response => response.json())
    .then(data => {
        const successBySex = data.success_by_sex;
        const labels = ['Male', 'Female']; // Update these labels according to your data
        const values = [
            successBySex.find(item => item.sexe === 'H').success_percentage,
            successBySex.find(item => item.sexe === 'F').success_percentage
        ];
        populatePieChart2(labels, values);

        const successBySpecialty = data.success_by_speciality;
        const labels1 = successBySpecialty.map(item => item.SPECIALITE);
        const values1 = successBySpecialty.map(item => item.success_percentage);
        populateLineChartSpecialty(labels1, values1);
        
        const successByYear = data.success_by_year;
        const yearLabels = successByYear.map(item => item.ANNEE);
        const yearValues = successByYear.map(item => item.success_percentage); // Use success_percentage instead of num_success
        populateDoughnutChartYear(yearLabels, yearValues); // Adjust the chart function accordingly

        const averageBySpeciality = data.average_moyenne_by_speciality;
        const specialtyLabelsAvg = averageBySpeciality.map(item => item.SPECIALITE);
        const avgValues = averageBySpeciality.map(item => item.avg_moyenne);
        populateLineChartSpecialty2(specialtyLabelsAvg, avgValues);

        const averageByYearSpeciality = data.average_moyenne_by_year_speciality;
        const yearLabels2 = Object.keys(averageByYearSpeciality);
        const avgValues2 = yearLabels2.map(year => averageByYearSpeciality[year].avg_moyenne);
        populateBarChartYear2(yearLabels2, avgValues2);

        const allMoyenneValues = data.all_moyenne_values; // Fetched 'moyenne' values
        createScatterChart(allMoyenneValues);

        const averageBySex = data.average_by_sexe;
        const sexLabelsAvg = averageBySex.map(item => item.sexe);
        const avgValuesSex = averageBySex.map(item => item.avg_moyenne);
        populatePieChart3(sexLabelsAvg, avgValuesSex);

    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });

  }

  function populatePieChart3(labels, values) {
    const genderChartCanvas = document.getElementById('average'); // Replace 'yourCanvasID' with your actual canvas ID

    new Chart(genderChartCanvas, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    // Add more colors as needed...
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: true,
                text: 'Success Percentage by Gender'
            }
        }
    });
}

  function createScatterChart(moyenneValues) {
    // Create a scatter chart using the fetched 'moyenne' values
    const ctx = document.getElementById('scatterChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Scatter Chart of Moyenne',
                data: moyenneValues.map((value, index) => ({ x: index, y: value })) // Assigning x and y values
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: true,
                text: 'Scatter Chart of Moyenne'
            },
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom'
                },
                y: {
                    type: 'linear',
                    position: 'left'
                }
            }
        }
    });
}

  function populateDoughnutChartYear(yearLabels, yearValues) {
    const ctx = document.getElementById('success-by-year-chart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: yearLabels,
            datasets: [{
                label: 'Success by Year',
                data: yearValues,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 255, 153, 0.6)',
                    'rgba(204, 255, 144, 0.6)'
                    // Add more colors as needed...
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 255, 153, 0.6)',
                    'rgba(204, 255, 144, 0.6)',
                    // Add more colors as needed...
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: true,
                text: 'Success by Year'
            },
            legend: {
                display: true,
                position: 'bottom' // You can adjust the position of the legend
            }
        }
    });
}


function populateBarChartYear2(yearLabels, avgValues) {
    const ctx = document.getElementById('averageByYearSpecialtyChart').getContext('2d');

    const averageByYearSpecialtyChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: yearLabels,
            datasets: [{
                label: 'Average Moyenne by Year',
                data: avgValues,
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            },
            title: {
                display: true,
                text: 'Average Moyenne by Year and Specialty'
            },
            legend: {
                display: false
            },
            tooltips: {
                callbacks: {
                    label: function (tooltipItem, data) {
                        const year = data.labels[tooltipItem.index];
                        const value = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
                        return `${year}: ${value.toFixed(2)}`;
                    }
                }
            }
        }
    });
}



function populateBarChartSpecialtyAverage(labels, values) {
    const ctx = document.getElementById('barChartSpecialtyAverage').getContext('2d');
    const barChartSpecialtyAverage = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Moyenne des moyennes par spécialité',
                data: values,
                backgroundColor: 'rgba(54, 162, 235, 0.5)', // Couleur du graphique
                borderColor: 'rgba(54, 162, 235, 1)',
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
}
function populateLineChartSpecialty2(labels, values) {
    const ctx = document.getElementById('lineChartSpecialty2').getContext('2d');
    const lineChartSpecialty = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Moyenne des moyennes par spécialité',
                data: values,
                fill: false,
                borderColor: 'rgba(255, 165, 0, 0.6)', // Couleur de la ligne
                borderWidth: 2
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}

function populateBarChartYear(labels, values) {
    const ctx = document.getElementById('success-by-year-chart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Success by Year',
                data: values,
                backgroundColor: 'rgba(75, 192, 192, 0.6)', // Adjust color as needed
                borderColor: 'rgba(75, 192, 192, 1)', // Adjust color as needed
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            },
            title: {
                display: true,
                text: 'Success by Year'
            },
            legend: {
                display: false
            }
        }
    });
}

function populateLineChartSpecialty(labels, values) {
    const specialtyChartCanvas = document.getElementById('success-per-specialty-line-chart');

    new Chart(specialtyChartCanvas, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Success Percentage per Specialty',
                data: values,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: true,
                text: 'Success Percentage per Specialty'
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}
function populatePieChartSpecialty(labels, values) {
    const specialtyChartCanvas = document.getElementById('success-per-specialty-chart');

    new Chart(specialtyChartCanvas, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    // Add more colors as needed...
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: true,
                text: 'Success Percentage per Specialty'
            }
        }
    });
}
function populatePieChart2(labels, values) {
    const genderChartCanvas = document.getElementById('gender-pie-chart');

    new Chart(genderChartCanvas, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: [
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 99, 132, 0.6)',
                    // Add more colors as needed...
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: true,
                text: 'Success Percentage by Gender'
            }
        }
    });
}
function populateBarChart(data) {
    const yearChartCanvas = document.getElementById('students-by-year-chart');
    const labels = data.map(item => item.ANNEE); // Assuming 'ANNEE' is for years
    const values = data.map(item => item.num_students); // Assuming 'num_students' is for student count

    new Chart(yearChartCanvas, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Students Enrolled',
                backgroundColor: 'rgba(54, 162, 235, 0.6)', // Adjust color as needed
                data: values,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            legend: { display: false },
            title: {
                display: true,
                text: 'Number of Students Enrolled by Year'
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

function populatePieChart(data) {
    const genderChartCanvas = document.getElementById('students-by-gender-chart');
    const labels = data.labels;
    const values = data.data;

    new Chart(genderChartCanvas, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    // Add more colors as needed...
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: true,
                text: 'Number of Students by Gender'
            }
        }
    });
}
function populateLineChart(data) {
    const specialtyChartCanvas = document.getElementById('students-by-specialty-chart');
    const labels = data.labels;
    const values = data.data;

    new Chart(specialtyChartCanvas, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Students by Specialty',
                borderColor: 'rgba(255, 99, 132, 0.6)', // Adjust line color as needed
                fill: false,
                data: values,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: true,
                text: 'Number of Students by Specialty'
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}


function loadTotals() {
    fetch('/total_counts')
        .then(response => response.json())
        .then(data => {
            const totalStudents = data.total_students;
            const totalSpecialties = data.total_specialties;
            const totalYears = data.total_years;
            const averageMoyenne = data.average_moyenne;

            const totalStudentsElement = document.getElementById('totalStudentsCount');
            totalStudentsElement.textContent = totalStudents;

            const totalSpecialtiesElement = document.getElementById('totalSpecialtiesCount');
            totalSpecialtiesElement.textContent = totalSpecialties;

            const totalYearsElement = document.getElementById('totalYearsCount');
            totalYearsElement.textContent = totalYears;

            const averageMoyenneElement = document.getElementById('averageMoyenne');
            averageMoyenneElement.textContent = averageMoyenne;
        })
        .catch(error => {
            console.error('Error fetching totals:', error);
        });
}


