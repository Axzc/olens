$("change-btn").click(function() {
    $.ajaxSetup({data: {csrfmiddlewaretoken: '{{ csrf_token }}'}});
    $.ajax({
        url:"/user/password-change",
        type:"post",
        dataType:'json',
        data:{
            "raw-pwd":$("#raw-pwd").val(),
            "new-pwd1":$("#new-pwd1").val(),
            "new-pwd2":$("#new-pwd2").val()
        },
        sucess:function (data) {
            console.log(data);
            var data = JSON.parse(data)
        }
    });
});