/**
 * @description 翻页组件
 * @author wulunyi
 */


define(['lib/jquery'],function ($) {
    $('head').append('<link rel="stylesheet" href="js/modules/page/page.css" />');
    var page = {
        init: function (dom, fn) {
            //存储初始化dom 元素与回调
            page._data.$dom = $(dom);
            fn && (page._data.fn = fn);
            //判定初始化事件（添加每页数量和总数量）
            $('body').bind('page:init', function (ev, pageSize, totalList) {
                page._init(pageSize, totalList);
            });
            //返回触发初始化事件钩子函数
            /**
             * @description 用于初始化翻页或则重新初始化
             * @param requestNum [String] 单次请求条数
             * @param totalNum [String] 请求数据总条数
             */
            return function (pageSize, totalList) {
                if(pageSize>=totalList){
                    $('#page_wrap').empty();
                }else{
                    //二次初始化时重置currentPage
                    page._data.currentPage = 0;
                    $('body').trigger('page:init', [pageSize, totalList]);
                }
            }
        },
        _data: {
            fn: null,
            $dom: null,//dom节点
            page: 0,//总页数
            totalList: 0,//总条数
            currentPage: 0,//当前页数
            showPage: 5//需要显示在翻页上的基础的页数
        },
        _init: function (pageSize, totalList) {
            pageSize = pageSize || 0;
            totalList = totalList || 0;
            //计算总也数(向上取整)
            if (!!pageSize) {
                page._data.page = Math.ceil(totalList / pageSize);
            }
            page._data.totalList = totalList;

            //渲染
            if (page._data.page > 0) {
                page._render();
            }else{
                page._data.page = 1;
                page._render();
            }
        },
        _render: function () {
            //默认为第一页
            page._goPage(1);
            //绑定翻页事件
            $('body').bind('page:go', function (ev, goPageNum) {
                page._goPage(goPageNum);
            });
        },
        _goPage: function (goPageNum) {

            //如果跳转为本页则不做处理
            if (page._data.currentPage == goPageNum) {
                return;
            }
            //若不为初始化则跳转执行回调
            if (page._data.currentPage != 0) {
                page._data.fn && page._data.fn(goPageNum);
            }

            page._data.currentPage = goPageNum;

            var isFirst = goPageNum == 1 ? "page-disabled" : "";//是否是第一页
            var isLast = goPageNum == page._data.page ? "page-disabled" : "";//是否至最后一页

            var html = '<ul class="page-tool-bar clearfix pull-right"><li><a href="javascript:;" class="pre-page ' + isFirst + '">上一页</a></li>';

            function showNormal(startPage, currentPage, size) {
                //公共选中样式
                var active = '';
                var html = '';
                for (var i = 0; i < size; i++) {
                    active = 'current-page';
                    if ((startPage + i) != currentPage) {
                        active = "";
                    }
                    html += '<li><a href="javascript:;" class="J-page-item ' + active + '"> ' + (startPage + i) + '</a></li>';
                }
                return html;
            }

            if (page._data.page > page._data.showPage) {
                if ((goPageNum - 3) < 0) {
                    html += showNormal(1, goPageNum, page._data.showPage);
                    html += '<li><a href="javascript:;">...</a></li>'
                }
                if (goPageNum == 4) {
                    html += '<li><a href="javascript:;" class="J-page-item "> 1</a></li>';
                }
                if (goPageNum == 5) {
                    html += '<li><a href="javascript:;" class="J-page-item "> 1</a></li>' +
                        '<li><a href="javascript:;" class="J-page-item "> 2</a></li>';
                }
                if (goPageNum >= 6) {
                    html += '<li><a href="javascript:;" class="J-page-item "> 1</a></li>' +
                        '<li><a href="javascript:;" class="J-page-item "> 2</a></li>' +
                        '<li><a href="javascript:;">...</a></li>';
                }
                if ((goPageNum - 3) >= 0 && (goPageNum + 2) < page._data.page) {
                    html += showNormal(goPageNum - 2, goPageNum, page._data.showPage);
                    html += '<li><a href="javascript:;">...</a></li>';
                }

                if ((goPageNum + 2) >= page._data.page) {
                    html += showNormal(page._data.page - page._data.showPage + 1, goPageNum, page._data.showPage);
                }
            } else {
                html += showNormal(1, goPageNum, page._data.page);
            }

            html += '<li><a href="javascript:;" class="next-page ' + isLast + '">下一页</a></li>' +
                '<li> 共' + page._data.page + '页，去第 <input type="text" class="page-input"/>页</li>' +
                '<li><button class="submit-page" style="padding: 0;border: none;">确定</button></li></ul>';

            page._data.$dom.html(html);

            page._data.$dom.find(".J-page-item").one('click', function (ev) {
                ev.preventDefault();
                var goPageNum = parseInt(ev.currentTarget.innerHTML);
                $('body').trigger('page:go', [goPageNum]);
            });
            page._data.$dom.find('.pre-page').one('click', function (ev) {
                ev.preventDefault();
                if (!isFirst) {
                    $('body').trigger('page:go', [page._data.currentPage-1]);
                }
            });
            page._data.$dom.find('.next-page').one('click', function (ev) {
                ev.preventDefault();
                if (!isLast) {
                    $('body').trigger('page:go', [page._data.currentPage+1]);
                }
            });
            page._data.$dom.find('.submit-page').on('click', function (ev) {
                ev.preventDefault();
                var index = parseInt($('.page-input').val());
                if (!!index && index > 0 && index <= page._data.page) {
                    $('body').trigger('page:go', [index]);
                }
            });

        }
    };

    return page;

});
