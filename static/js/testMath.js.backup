Date.prototype.Format = function (fmt) {
    var o = {
        "M+": this.getMonth() + 1, //月份
        "d+": this.getDate(), //日
        "H+": this.getHours(), //小时
        "m+": this.getMinutes(), //分
        "s+": this.getSeconds(), //秒
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度
        "S": this.getMilliseconds() //毫秒
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}


function showTest() {
    $("#num1").text(data.num1);
    $("#num2").text(data.num2);
    $("#operation").text(data.operation);
    $("#uanswer").val("");
    $("#uanswer").focus();
    $("#angel").text(data.which_angel);
    $("#num").html(num += 1);
}

function startTest() {
    start_time = new Date();
    $('#nextTest').removeAttr("disabled");
    $('#uanswer').attr("readonly", false).focus();
    $("#endText").removeAttr("disabled");
}
