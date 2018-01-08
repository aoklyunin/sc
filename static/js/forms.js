
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
  if (form.find(".commentContent").html()!=''){
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

    var fd = new FormData(data);
    fd.append('commentContent', commentContent);
    fd.append('image',$form.find(".imageFileInput").prop('files')[0]);
    fd.append('parentType', data.parentType);
    fd.append('parentId', data.parentId);

    jQuery.ajax({
        url:url,
        data: fd,
        cache: false,
        contentType: false,
        processData: false,
        method: 'POST',
        type: 'POST', // For jQuery < 1.9
        success: function(data){
            location.reload();
        }
    });
   // var doPost = $.post(url, {
   //     parentType: data.parentType,
   //     parentId: data.parentId,
   //     commentContent: commentContent,
   //     image: form.find(".imageFileInput").val(),
   // });


   // doPost.done(function (response) {
        //var errorLabel = $form.find("span#postResponse");
        //if (response.msg) {
        //    errorLabel.text(response.msg);
        //    errorLabel.removeAttr('style');
        //}
   //     location.reload();
   // });
  }
}


$("#commentForm").submit(function (event) {
    submitEvent(event, $(this));
});


$("#addSmiles").click(function(){
  saveSelection();
  var pos = $(this).position();
  $("#smilePanel").css({ top: pos.top, left: pos.left});
  $("#smilePanel").show();
});


$("#closeSmilePanel").click(function(){
  $("#smilePanel").hide();
});

$(".smileImg").click(function(){
    //restoreSelection(true);
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
             saveSelection();
            var pos = $(this).position();
            $("#smilePanel").css({ top: pos.top, left: pos.left});

            $("#smilePanel").show();

        });


function insertTextAtCursor(text) {
    var sel, range, html;
    if (window.getSelection) {
        sel = window.getSelection();
        if (sel.getRangeAt && sel.rangeCount) {
            range = sel.getRangeAt(0);
            range.deleteContents();
            range.insertNode( document.createTextNode(text) );
        }
    } else if (document.selection && document.selection.createRange) {
        document.selection.createRange().text = text;
    }
}


function saveSelection() {
    if (window.getSelection) {
        sel = window.getSelection();
        if (sel.getRangeAt && sel.rangeCount) {
            return sel.getRangeAt(0);
        }
    } else if (document.selection && document.selection.createRange) {
        return document.selection.createRange();
    }
    return null;
}

function restoreSelection(range) {
    if (range) {
        if (window.getSelection) {
            sel = window.getSelection();
            sel.removeAllRanges();
            sel.addRange(range);
        } else if (document.selection && range.select) {
            range.select();
        }
    }
}
