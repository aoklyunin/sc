
function submitSubmitEvent(event, form) {
    checked = $("#formChecked").is(':checked');
    if (!checked){
        event.preventDefault();
        var choices = $("#id_ctp").val();
        var flgGo;
        if (choices==null){
            flgGo=true;
        }else{
            flg = true;
            for (var i=0;i<choices.length;i++){
                var c = choices[i];
                if (c==1 || c==2 || c ==5)
                    flg = false;
            }
            var flgGo = flg;
            if (!flg){
                if (!$("#id_url").val()){
                    flgGo = confirm("Выбранные Вами категории предполагают ссылку на внешний ресурс. Вы уверены, что она Вам не нужна?");
                }else{
                    flgGo = true;
                }
            }
        }
        if (flgGo){
            $("#formChecked").prop('checked', true);;
            form.submit()
        }
    }
}

function editProfileEvent(event, form) {
    checked = $("#formChecked").is(':checked');
    if (!checked){
       $("#formChecked").prop('checked', true);
       $("#aboutField").val($("#ceAbout").html());
       //alert( form.about_text);
       form.submit();
    }
}

function editPostEvent(event, form) {
    checked = $("#formChecked").is(':checked');
    if (!checked){
       $("#formChecked").prop('checked', true);
       $("#postField").val($("#cePost").html());
       form.submit();
    }
}

function submitEvent(event, form) {
    event.preventDefault();
    var $form = form;
    var data = $form.data();
    url = $form.attr("action");
    commentContent = $form.find(".commentContent").html();
    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var doPost = $.post(url, {
        parentType: data.parentType,
        parentId: data.parentId,
        commentContent: commentContent
    });


    doPost.done(function (response) {
        //var errorLabel = $form.find("span#postResponse");
        //if (response.msg) {
        //    errorLabel.text(response.msg);
        //    errorLabel.removeAttr('style');
        //}
        location.reload();
    });
}


$("#commentForm").submit(function (event) {
    submitEvent(event, $(this));
});


$("#addSmiles").click(function(){
  var pos = $(this).position();
  $("#smilePanel").css({ top: pos.top, left: pos.left});
  $("#smilePanel").show();
});


$("#closeSmilePanel").click(function(){
  $("#smilePanel").hide();
});

$(".smileImg").click(function(){
    targetId = $(this).attr('target-id');
    $("#"+targetId).append('<img src="'+$(this).attr('src')+'">');
});


$("#ceAbout").html($("#aboutField").val());

$("#cePost").html($("#postField").val());

$("#editProfileForm").submit(function (event) {
    editProfileEvent(event, $(this));
});

$("#editPostForm").submit(function (event) {
    editPostEvent(event, $(this));
});

$("#submitForm").submit(function (event) {
    submitSubmitEvent(event, $(this));
});


$(".addSmilesTree").click(function(){
            var pos = $(this).position();
            $("#smilePanel").css({ top: pos.top, left: pos.left});
            $("#smilePanel").show();
        });

