let trendsChartColors = ['#2760b1', '#f683df', '#639c4a'];

let trendsChartOptions = {tooltips: {
    enabled: true
},
hover :{
    animationDuration:0
},
scales: {
    xAxes: [{
        ticks: {
            beginAtZero:true,
            fontFamily: "'Open Sans Bold', sans-serif",
            fontSize:11
        },
        scaleLabel:{
            display:false
        },
        gridLines: {
        }, 
        stacked: true
    }],
    yAxes: [{
        gridLines: {
            display:true,
            color: "#fff",
            zeroLineColor: "#fff",
            zeroLineWidth: 0
        },
        scaleLabel:{
            display:false
        },
        ticks: {
            fontFamily: "'Open Sans Bold', sans-serif",
            fontSize:11
        },
        stacked: true
    }]
},
legend:{
    display:true
},

animation: {
    onComplete: function () {
        var chartInstance = this.chart;
        var ctx = chartInstance.ctx;
        ctx.textAlign = "left";
        ctx.font = "9px Open Sans";
        ctx.fillStyle = "#fff";

        Chart.helpers.each(this.data.datasets.forEach(function (dataset, i) {
            var meta = chartInstance.controller.getDatasetMeta(i);
            Chart.helpers.each(meta.data.forEach(function (bar, index) {
                data =  dataset.data[index];
                /* if(i==0){
                    ctx.fillText(data, 50, bar._model.y+4);
                } else {  */
                if ( data != 0 ) ctx.fillText(data, bar._model.x - 15, bar._model.y);                // }
            }),this)
        }),this);
    }
},
pointLabelFontFamily : "Quadon Extra Bold",
scaleFontFamily : "Quadon Extra Bold",
};


let ctxTrends = document.getElementById('trendsChart').getContext('2d');

let trendsChart = new Chart(ctxTrends, {
    type: 'horizontalBar',
    data: {
        labels: [],
        datasets:[{
            label:'Occupied',
            data: [],
            backgroundColor: "#18A2B8",
            hoverBackgroundColor: "#18A2B8",
        },{
            label:'Free',
            data: [],
            backgroundColor: "#28A745",
            hoverBackgroundColor: "#28A745",
        },{
            label:'Unusable',
            data: [],
            backgroundColor: "#DC3545",
            hoverBackgroundColor: "#DC3545",
        },]
    },
    options: trendsChartOptions
});

function updateTrendsChart(res) {

    trendsChart.destroy();
    trendsChart = new Chart(ctxTrends, {
        type: 'horizontalBar',
        data: {
            labels: res.labels,
            datasets:[{
                label:'Occupied',
                data: res.occupied,
                backgroundColor: "#18A2B8",
                hoverBackgroundColor:  "#158596",
            },{
                label:'Free',
                data: res.free,
                backgroundColor: "#28A745",
                hoverBackgroundColor:  "#1c7531",
            },{
                label:'Unusable',
                data: res.unusable,
                backgroundColor: "#DC3545",
                hoverBackgroundColor:"#802029",
            },]
        },
        options: trendsChartOptions
    });

}
