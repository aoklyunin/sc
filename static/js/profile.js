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
     $("#modalAddress").text($(this).attr('href'));
     $("#modalAddress").attr('href',$(this).attr('href'));
     $(".goLink").attr('href',$(this).attr('href'));
     $(".copyLink").attr('href',$(this).attr('href'));
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

});
