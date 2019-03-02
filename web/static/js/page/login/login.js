require.config({
    baseUrl: 'js/'
});

require([ 'util/request', 'lib/jquery', 'modules/template/endless/endless','lib/basic/bootstrap'],
    function ( request, $) {
    var login = {
        init: function () {
            $('#J_login').on('click', function (e) {
                e.preventDefault();
                login.login();

            });
        },
        login: function () {
            var params = {
                name: '',
                password: ''
            };

            params.name = $('#J_username').val();
            params.password = $('#J_password').val();
            $('#J_login--errorText').css('display', 'none');
            request.post('login', params, function (rsp) {

                // rsp = JSON.parse(rsp);

                if (rsp.code == 1) {

                        window.location.href = './showTrainAuc.html';
                        console.log('登陆成功');
                    } else {
                        $('#J_login--errorText').css('display', 'inline');
                    }
                }

            )
        }
    };
    login.init();


});







