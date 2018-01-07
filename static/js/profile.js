    $('a#editProfile').click(function (e) {
    if ( $(this).text() != "Выйти"){
      e.preventDefault();
    }
    $(this).text("Выйти");
    $(this).attr('href', '/logout/');
});

$('a.socialImg').click(function (e) {
    //if ( $(this).text() != "Выйти"){
     e.preventDefault();
     url = $(this).attr('href');
     title = $(this).find('img').attr('title');
     if (title=='Tel' || title=='E-mail'){
        $(".goLink").hide();
         $("#modalAddress").attr('href','');
     }else{
        $(".goLink").attr('href',$(this).attr('href'));
        $(".goLink").show();
        $("#modalAddress").attr('href',url);
     }
     $(".copyLink").attr('href',url);
     $("#modalAddress").text(title+": "+url);
     $("#myModal").modal();
   // }
   // $(this).text("Выйти");
   // $(this).attr('href', '/logout/');
});

$('.copyLink').click(function (e) {
    e.preventDefault();
    $('#TmpTextarea').text($(this).attr('href'));
    $('#TmpTextarea').select();

    try {
      var successful = document.execCommand('copy');
      var msg = successful ? 'successful' : 'unsuccessful';
      console.log('Copying text command was ' + msg);
    }   catch (err) {
      console.log('Oops, unable to copy');
    }
    $("#myModal").modal('hide');

});

$('.goLink').click(function(e){
    e.preventDefault();
    var win = window.open($(this).attr('href'), '_blank');
    win.focus();
});




