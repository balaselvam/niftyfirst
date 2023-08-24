
//chart - 1 (Open Interest):
$(document).ready(function () {
    const config = {
        type: 'line',
        data: {
            labels: Array(30).fill("00:00:00"),
            datasets: [{
                label: "OI PCR",
                backgroundColor: 'white',
                borderColor: 'black',
                fontColor: 'white',
                data: Array(30).fill(null),
                fill: true,
                tension: 0.3,
                segment: {
                    borderColor: context => up(context, '#00ff1796') || down(context, '#fd05398a'),
                    backgroundColor: context => up(context, '#00ff1796') || down(context, '#fd05398a'),
                }
            }],
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'OPEN INTEREST',
                    color: 'white'
                },
                legend: {
                    labels: {
                        color: 'white'
                    }
                },
                chartAreaBorder: {
                    borderColor: 'white',
                    borderWidth: 2,
                    borderDash: [1, 1],
                    borderDashOffset: 2,
                }
            },
            animations: {
                radius: {
                    duration: 400,
                    easing: 'linear',
                    loop: (context) => context.active
                }
            },
            hoverRadius: 14,
            hoverBackgroundColor: 'yellow',
            interaction: {
                mode: 'nearest',
                intersect: false,
                axis: 'x'
            },

            tooltips: {
                enabled: false,
                position: 'nearest',
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        type: 'time',
                        text: 'TIME',
                        color: 'white',
                        font: {
                            family: 'Verdana',
                            size: 20,
                            weight: 'bold',
                            lineHeight: 1.2,
                        },
                        padding: {top: 20, left: 0, right: 0, bottom: 0}
                    },
                    border: {
                    color: 'white'
                    },
                    ticks: {
                        color: 'white'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'OI - PCR',
                        color: 'white',
                        font: {
                            family: 'Verdana',
                            size: 20,
                            style: 'normal',
                            lineHeight: 1.2
                        },
                        padding: {top: 30, left: 0, right: 0, bottom: 0}
                    },
                    border: {
                    color: 'white'
                    },
                    //min: 0,
                    //max: 100,
                    ticks: {
                    // forces step size to be 50 units
                    stepSize: 0.001,
                    color: 'white'
                    }
                }
            }
        },
        plugins: [chartAreaBorder]
    };

    const context = document.getElementById('canvas').getContext('2d');

    const up = (context, value) => context.p0.parsed.y < context.p1.parsed.y ? value : undefined;
    const down = (context, value) => context.p0.parsed.y > context.p1.parsed.y ? value : undefined;

    const maxDataPoints = 30; 
    const lineChart = new Chart(context, config);

    const source = new EventSource("/chart-data");

    source.onmessage = function (event) {
        const data = JSON.parse(event.data);
        const newTime = data.curr_time;
        //console.log(data);
        // Check if the newTime already exists in the labels array
        if (!config.data.labels.includes(newTime)) {
            // Remove the first data point if the array length exceeds 30
            if (config.data.labels.length === maxDataPoints) {
                config.data.labels.shift();
                config.data.datasets[0].data.shift();
                //config.data.datasets[1].data.shift();
            }
            // Add the newTime and data point to the arrays
            config.data.labels.push(newTime);
            config.data.datasets[0].data.push(data.oi_pcr_avg);
            //config.data.datasets[1].data.push(data.spot_price_change);
            lineChart.update();
        }
    }
});

// chart -2 (price):
$(document).ready(function () {
    const config1 = {
        type: 'line',
        data: {
            labels: Array(30).fill("00:00:00"),
            datasets: [
            {
                label: "PRICE_CHANGE",
                backgroundColor: 'white',
                borderColor: 'black',
                data: Array(30).fill(null),
                fill: true,
                tension: 0.3,
                segment: {
                    borderColor: context => up(context, '#00ff1796') || down(context, '#fd05398a'),
                    backgroundColor: context => up(context, '#00ff1796') || down(context, '#fd05398a'),
                }
                
            }],
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'CASH- INDEX',
                    color: 'white'
                },
                legend: {
                    labels: {
                        color: 'white'
                    }
                },
                chartAreaBorder: {
                    borderColor: 'white',
                    borderWidth: 2,
                    borderDash: [1, 1],
                    borderDashOffset: 2,
                }
            },
            animations: {
                radius: {
                    duration: 400,
                    easing: 'linear',
                    loop: (context) => context.active
                }
            },
            hoverRadius: 14,
            hoverBackgroundColor: 'yellow',
            interaction: {
                mode: 'nearest',
                intersect: false,
                axis: 'x'
            },

            tooltips: {
                enabled: false,
                position: 'nearest',
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        type: 'time',
                        text: 'TIME',
                        color: 'white',
                        font: {
                            family: 'Verdana',
                            size: 20,
                            weight: 'bold',
                            lineHeight: 1.2,
                        },
                        padding: {top: 20, left: 0, right: 0, bottom: 0}
                    },
                    border: {
                    color: 'white'
                    },
                    ticks: {
                        color: 'white'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'PRICE',
                        color: 'white',
                        font: {
                            family: 'Verdana',
                            size: 20,
                            style: 'normal',
                            lineHeight: 1.2
                        },
                        padding: {top: 30, left: 0, right: 0, bottom: 0}
                    },
                    border: {
                    color: 'white'
                    },
                    //min: 0,
                    //max: 100,
                    ticks: {
                    // forces step size to be 50 units
                    stepSize: 0.001,
                    color: 'white'
                    }
                }
            }
        },
        plugins: [chartAreaBorder]
    };

    const context1 = document.getElementById('canvas1').getContext('2d');
    const up = (context, value) => context.p0.parsed.y < context.p1.parsed.y ? value : undefined;
    const down = (context, value) => context.p0.parsed.y > context.p1.parsed.y ? value : undefined;
    const lineChart1 = new Chart(context1, config1);

    const source = new EventSource("/chart-data");

    source.onmessage = function (event) {
        const data = JSON.parse(event.data);
        const newTime = data.curr_time;
        
        if (!config1.data.labels.includes(newTime)) {
            if (config1.data.labels.length === 30) {
                config1.data.labels.shift();
                //config1.data.datasets[0].data.shift();
                config1.data.datasets[0].data.shift();
            }
            config1.data.labels.push(newTime);
            //config1.data.datasets[0].data.push(data.oi_pcr_avg);
            config1.data.datasets[0].data.push(data.spot_price_change);
            lineChart1.update();
        }
    }
});

// creating chartborder style 
const chartAreaBorder = {
    id: 'chartAreaBorder',
    beforeDraw(chart, args, options) {
        const {ctx, chartArea: {left, top, width, height}} = chart;
        ctx.save();
        ctx.strokeStyle = options.borderColor;
        ctx.lineWidth = options.borderWidth;
        ctx.setLineDash(options.borderDash || []);
        ctx.lineDashOffset = options.borderDashOffset;
        ctx.strokeRect(left, top, width, height);
        ctx.restore();
    }
};
