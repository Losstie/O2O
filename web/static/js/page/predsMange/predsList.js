/**
 * Created by Adu on 2017/1/19.
 */
/*********************************************
 * 用途:获取导师列表，并且实现查询，新增导师功能（这部分跳转到tutorDetail.js）
 * 子模块：listService.js
 * *******/
require.config({
    baseUrl: 'js/'
});

require(['lib/jquery',  'util/request', 'modules/page/page', 'util/Headertip', 'modules/baseModule','page/predsMange/listService' ,'lib/juicer','util/juicerHelper','modules/time'],
    function($, request, page, headertip, baseModule, listSer){

        var index = {

            init: function() {

                var goPage = page.init('#page_wrap', function (num) {

                    var _params = index.params;
                    console.log('查询' + num + '页');
                    _params.page = num;
                    index.getList(_params);
                });

                page.initPage = goPage;//初始化，存储下page实例方法
                $('body').one('pageSet', function (ev, num, total) {
                    goPage(num, total);
                });

                baseModule();
                this.getList(this.params);
                this.search();
                this.logout();

            },

            params:{
                page: '',
                userId:'',
                couponId:'',
                dateReceivedTime: ''
            },

            // 获取导师列表
                getList:function(params) {
                    listSer.getTutorList(params,function(rsp) {

                        rsp = JSON.parse(rsp);
                        console.log(rsp);
                        if(rsp.code == 1) {
                            var rows = rsp.data.rows;
                            var tpl = listSer.tutorListTpl();
                            var tutorListStr = juicer(tpl, rsp.data);


                            $('#J_show').html(tutorListStr);
                            $('#J_count').html(rows);
                            //    初始化分页
                            $('body').trigger('pageSet', [10, rows]);

                        }

                    });
                },
                /**
                * @decription 搜索功能
                 * @author dujiahao
                * */
                search: function() {

                    $('#J_search').on('click', function(event) {

                        event.preventDefault();

                        var _params = index.params;

                        _params.page = 1;
                        _params.userId = $("#J_userId").val();
                        _params.couponId = $('#J_couponId').val();
                        _params.dateReceivedTime = $('#J_dateReceivedTime').val();

                        var goPage = page.init('#page_wrap', function(num) {

                            var _params = index.params;
                            _params.page = num;
                            index.getList(_params);
                        });
                        $('body').one('pageSet', function (ev, num, total) {
                            goPage(num, total);

                        });
                        index.getList(_params);
                    });
                },
                /**
                * @decription 注销登录
                 * @author dujiaho
                * */
                logout:function() {

                    $('#J_logout').on('click', function(event) {

                        event.preventDefault();
                        listSer.logout();

                    });
                },

        };

    index.init();
    console.log(111);

});