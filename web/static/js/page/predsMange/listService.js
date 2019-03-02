/**
 * Created by Adu on 2017/2/8.
 */
/**
 * @decription 导师列表页服务  实现ajax请求及模板提供
 *@author dujiahao
 * 服务于 tutorList.js
 * */


define(['util/funcTpl', 'util/request','api/api.config'],
    function(funcTpl, request, API) {

        var listSer = {

        getTutorList: function(data, callback) {

            request.post(API.getpredsList, data, function(rsp) {

                callback(rsp);
            }
            );

        },
        logout:function() {

            request.post(API.logout, function() {

                window.location.href = './login.html';
            });
        },
        tutorListTpl:function() {
            var str = '{@each list as item}' +
                    '<tr>' +
                        '<td>${item.tutorId}</td>' +
                        '<td>${item.onlineTime | handleTime}</td>' +
                        '<td>${item.tutorName}</td>' +
                        '<td>${item.tutorSex | handleSex}</td>' +
                        '<td>${item.tutorNumber}</td>' +
                        '<td>${item.price}/h</td>' +
                        '<td>${item.meetNumber}</td>' +
                        '<td>${item.operateName}</td>' +
                        '<td>${item.operateNumber}</td>' +
                        '<td>'+
                            '<a href="./tutorDetail.html?td=${item.tutorId}"  class="btn btn-xs btn-info"><i class="fa fa-file-text-o"></i>详情</a>'+
                        '</td>' +
                    '</tr>' +
                    '{@/each}';

            return str;

        }

    };

        return  listSer;

    });