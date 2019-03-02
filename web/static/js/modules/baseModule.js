/**
 *  jipeng
 *  2015.05.26
 *  所有页面必须引入
 * **/

define(['lib/basic/bootstrap','modules/template/endless/endless','util/request','lib/juicer'],function(bs,en,request){
    var base = {
        init: function () {
            // 清除样式
            var firstMenu = $('.main-menu > ul > li');
            var secondMenu = firstMenu.find('ul > li');


            firstMenu.removeClass('active opened');
            secondMenu.find('li').removeClass('active');
            // 根据 uri 高亮样式
            var url = {
                "/": [0,-1],
                "/contentList": [6,0],
                "/contentEdit": [6,1],
                "/filedEdit": [6,2],
                "/orderBank":[4,0],
                "/entryMoney":[7,0],
                "/outMoney":[7,0]
            };
            var key = url[window.currentPath];
            // 一级菜单
            if(key){
                var first = firstMenu.eq(key[0]).addClass('openable open');//高亮一级领域
                if (key[1] != -1) {
                    // 二级菜单
                    var second = first.find('ul');
                    second.show('slow');
                }
            }
        },
        _autoFunction:function(){
            this._setPubFun();
            this._setPubData();
        },
        _setPubData:function(){
            window.pub = {
                userImg:"/static/image/page/defaultUserImg.png",
                imgServer:"http://103.37.148.131:3389/"
            }
        },
        //添加全局函数
        _setPubFun:function(){
            //1.防止重复点击。一段时间内，只会触发第一次点击
                $.extend({
                    clickOnce:function(dom,fn,time){
                        var lazyTime = time || 3;//默认延迟3s内点击无效
                        var clickTime;//可点击时间
                        if(!dom){return}  

                        $(dom).click(function(){
                            var nowTime = new Date().getTime();
                            //第一次点击时，初始化点击时间,并且执行函数
                            if (!clickTime) {
                                clickTime = new Date().getTime()+ lazyTime*1000;

                                //记得修改处理函数的this指针，否则在fn内指向window
                                fn.apply(this)
                            };
                            //如果点击时间大于当前时间，则返回
                            if(clickTime>nowTime){
                                return
                            }else{
                                clickTime = null
                            }
                        });
                    }
                });

            $.extend({
                strTrim:function(dom){
                    if(!dom){return}

                    var value = $(dom).val();
                    if(value){
                        value = value.trim();
                    }else{
                        value = ""
                    }
                    return value;
                }
            });
            //2.处理毫秒级的时间
                $.extend({
                    handleTime:function(times){
                        var nowTime = new Date(times),
                            year    =  nowTime.getFullYear(),
                            month   =  nowTime.getMonth(),
                            day     =  nowTime.getDate();

                        return year+'.'+month+"."+day;    

                    }
                });   
                juicer.register('handleTime',$.handleTime); 

            //3.

        }

    };

    base._autoFunction();

    return base.init;

   /*var base = {
        init :function(){
            this._getAllLimitsPageByUser();
        },
         //取得用户对应的权限
        _getAllLimitsPageByUser:function(){
            request.post("/userManage/getStuffLimitPageByStuffId",{},function(ret){
                if(1 == ret.code){
                	 var limitParent = [];
                     var limitpage = [];
                       var data = ret;
                         for(var i  = 0; i < data.data.length; i++){
                             limitParent.push({
                                 pid:data.data[i].limits_pid,
                                 pname:data.data[i].limits_pname,
                                 childLimit:[]
                             });
                         }
                         limitpage = base.arrayUnique(limitParent);
                         for(var i  = 0; i < limitpage.length; i++) {
                             for (var j = 0; j < data.data.length; j++) {
                                 if (data.data[j].limits_pid == limitpage[i].pid) {
                                     limitpage[i].childLimit.push(data.data[j]);
                                 }
                             }
                         }
                    data.data = limitpage;
                    var url = $("#J-pages").attr("data-url");//当前页面的url
                    var tpl =  '{@each data as Item,index}'+
                                 ' <li class="openable">'+
                                  '   <a href="javascript:;" class="J-btn-toggle">'+
                                  '     <span class="menu-icon">'+
                                 '       <i class="fa fa-tag fa-lg"></i>'+
                                 '       </span>'+
                                 '       <span class="text">'+
                                 '       <%=Item.pname%>'+
                                 '        </span>'+
                                 '        <span class="menu-hover"></span>'+
                                 '     </a>'+
                                 '     <ul class="submenu"${Item.childLimit|display_bulid}>'+
                                      '{@each Item.childLimit as Item1}'+
                                       '<li><a href="<%=Item1.limits_url%>" ${Item1|links_build}><span class="submenu-label"><%=Item1.limits_name%></span></a></li>'+
                                      '{@/each}'+
                                 '     </ul>'+
                                 '   </li>'+
                                 '{@/each}';
                    
                    var links = function(data) {
                    	if(data.limits_url == url){
                    		return 'class=active';
                    	}else{
                    		return "";
                    	}
                    };
                    
                    var display = function(data){
                    	for(var i = 0; i < data.length; i++){
                    		if(data[i].limits_url == url){
                        		return 'style=display:block';
                        	}
                    	}
                    };
                    juicer.register('display_bulid', display); 
                    juicer.register('links_build', links); 
                    var temp = juicer(tpl,data);
                    $("#J-pages").append(temp);
                     $(".J-btn-toggle").click(function(){
                         var sbmenu = $(this).parent().find(".submenu").toggle();
                     });

                }

            });
        },
        arrayUnique:function(arr) {
            function has(array,data){
                for(var k = 0; k < array.length;k++){
                    if(data == array[k].pid){
                        return true;
                    }
                }
                return false;
            }
            var tmp = [];
            tmp.push(arr[0]);
            for(var i = 1; i < arr.length; i++){
                if(has(tmp,arr[i].pid) == false){
                    tmp.push(arr[i]);
                }
            }
            return tmp;
        }
   };
    base.init();*/
});