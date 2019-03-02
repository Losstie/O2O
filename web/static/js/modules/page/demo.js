require(['page','jquery'], function ( page) {
    //正常使用
    page.init('.hello', function (num) {
        console.log(num);//回调num 为即将跳转的页数
    })(10,70);

    //调用page.init 返回钩子函数，可用于根据新参数构建新翻页
   /* var demo = page.init('.hello', function (num) {
        console.log(num);
    });
    demo(10,100);*/

    //重置
    //demo(10,30);
});
