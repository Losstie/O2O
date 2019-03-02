
console.log("数据");
var socket = io();
var myChart = echarts.init(document.getElementById('main'));
option = {
    title: {
        text: 'XgBoost模型训练: train-auc变化详情'
    },
    tooltip: {},
    legend: {
        data:['train-auc']
    },
    xAxis: {
        type: 'category',
        data: []
    },
    yAxis: {
        type: 'value',
        scale: true
    },
    series: [{
        name:'train-auc',
        data: [],
        type: 'line',
        smooth: true
    }]
};
myChart.setOption(option);
socket.on('news', function (data) {

    console.log(data);
        myChart.setOption({
        xAxis: {
            data: data.rounds
        },
        series: [{
            name: 'train-auc',
            data: data.auc
        }]
    });

});