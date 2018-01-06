
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




$("#submitForm").submit(function (event) {
    submitSubmitEvent(event, $(this));
});

$("#ceAbout").html($("#aboutField").val());
$("#aboutField").val()

$("#editProfileForm").submit(function (event) {
    editProfileEvent(event, $(this));
});


