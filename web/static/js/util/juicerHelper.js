require.config({
    baseUrl: 'js/'
});

require(['lib/juicer'], function () {
    var helper = {
        init: function () {
            juicer.register('handleTime', helper.handleTime);
            juicer.register('handleState', helper.handleState);
            juicer.register('handleSex', helper.handleSex);

        },
        // 处理毫秒级的时间
        handleTime: function (times) {
            var t = new Date(times);
            return t.getFullYear() + '年' + (t.getMonth() + 1) + '月' + t.getDate() + '日 ' + t.toTimeString().slice(0, 5)
        },
        // 处理状态
        handleState: function (state) {

            var _state = state;
            switch(_state){

                case 0:
                    return '待付款';
                    break;
                case 1:
                    return '待协商';
                    break;
                case 2:
                    return '退款中';
                    break;
                case 3:
                    return '已退款';
                    break;
                case 4:
                    return '待开始';
                    break;
                case 5:
                    return '进行中';
                    break;
                case 6:
                    return '待评价';
                    break;
                case 7:
                    return '已评价';
                    break;
                case 8:
                    return '已关闭';
                    break;
            }

        },

        handleSex:function(sex){
            var map = {
                0:'未知',
                1:'男',
                2:'女'
            };

            return map[sex];
        }



    };
    helper.init();
});