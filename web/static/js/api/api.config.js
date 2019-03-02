/**
 * Created by Adu on 2017/1/19.
 */
/**********************************************
* 用途：统一管理整站api地址，减少代码冗余
* 通过require.js调用
* */
define(function(){

    return {
        getpredsList:'/getList', // 获取预测列表
        logout:'/logout', // 注销
        login:'login'   // 登录
    };
});