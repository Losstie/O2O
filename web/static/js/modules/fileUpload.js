/**
 * 文件上传
 * Created by WXY on 2016/1/25.
 */
require.config({
    baseUrl :  'js/'
});
define(['lib/jquery', 'util/Headertip', 'modules/ajaxfileupload'], function ($, headertip) {



    $.fn.extend({
        "ajaxfileuploadPic": function (opt) {
            $(this).click(function(){
                var url = opt.url || "",
                //data= opt.data || {data:""},
                    file = $(this).attr("data-file")? "#"+$(this).attr("data-file") : "",
                    preview = $(this).attr("data-preview") ? "#"+$(this).attr("data-preview") : $(this).find(".preview");
                if(file == ""){
                    if(window.console) console.log("没有给上传按钮制定:data-file属性");
                    return;
                }

                $(file).click();
                $(file).change(function(){



                    if( $(file).val() != ""){
                        if(!/\.jpg$|\.jpeg$|\.gif$|\.png$/i.test($(file).val())){
                            headertip.error("上传图片格式不正确,请确保是gif,png,jpeg,jpg图片");
                            $(file).val("");
                            return;
                        }
                        headertip.info("图片上传中,请稍等...");
                        //if(opt.callbackPre && typeof opt.callbackPre === "function")  opt.callbackPre();
                        $.ajaxFileUpload({
                            url:url,            //需要链接到服务器地址
                            secureuri:false,
                            fileElementId:$(file).attr("id"),   //文件选择框的id属性
                            dataType: 'json',
                            success: function(res){
                                var data = res.data;
                                // $(preview).attr("src",BEEN.imgServer+data.url); // 暂时不改图片地址
                                $(preview).show();
                                if(opt.callback){
                                    opt.callback(data,preview);
                                }
                                headertip.success("图片上传成功",2000,true);
                            },
                            error: function (data, status, e)
                            {
                                headertip.error("上传失败:"+e);
                            }
                        });
                    }
                });
            });
        }
        // // 上传文档
        // "ajaxfileuploadDoc":function(opt) {
        //
        //
        //
        //
        // }
    });

});

