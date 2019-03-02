
var myChart = echarts.init(document.getElementById('main'));
var option = {
            title: {
                text: '算法模型效果对比'
            },
            tooltip: {},
            legend: {
                data:['auc']
            },
            xAxis: {
                data: ["XgBoost","SVM","RF","LR"]
            },
            yAxis: {
                scale:true

            },
            series: [{
                name: 'auc',
                type: 'bar',
                label: {
                    normal: {
                        show: true,
                        position: 'top'
                    }
            },
                data: [0.78930136,0.64157072,0.77637144,0.765072524]
            }]
        };
myChart.setOption(option);

