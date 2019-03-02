
var user = {
    name:'losstie',
    password:'123456'

};
var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var fs = require('fs');
var file="F:\\Project\\FinaDesigner_Dujiahao\\auc_change.json";


app.use(express.static('../static'));

// 登录
app.post('/login', function(req, res){
    var response = {"code":1};
    req.on('data',function(data){
        var a = data.toString();
        var b = a.split('&');
        var c = b[0].split('=');
        var d = b[1].split('=');
        if(c[1]==user.name && d[1] == user.password){
            res.send(response);
        }
    });
});
var data = {
    auc:[0.840627, 0.854662, 0.863224],
    rounds:[1,2,3]
};

io.on('connection', function (socket) {
    setInterval(function(){
        var result=JSON.parse(fs.readFileSync( file));

        data.auc = [].concat(result.history_auc);
        data.rounds = [].concat(result.history_rouns);
        socket.emit('news',data);
    },5000)

});


http.listen(3000, function(){
  console.log('listening on *:3000');
});