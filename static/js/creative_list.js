
    $(document).ready(function(){
      // нормальные пропорции фрейма ютуба
      $( ".ytframe" ).each(function( index ) {
        $( this ).height( $( this ).width()*9/16 );
      });
      // вешаем обработки прокрутки колесиком мыши
      var elem = document.getElementsByClassName('creativeListBody')[0];
      if (elem.addEventListener) {
        if ('onwheel' in document) {
          // IE9+, FF17+, Ch31+
          elem.addEventListener("wheel", onWheel);
        } else if ('onmousewheel' in document) {
          // устаревший вариант события
          elem.addEventListener("mousewheel", onWheel);
        } else {
          // Firefox < 17
          elem.addEventListener("MozMousePixelScroll", onWheel);
        }
      } else { // IE8-
        elem.attachEvent("onmousewheel", onWheel);
      }
    });
    // сам обработчик
    function onWheel(e) {
      $('.delimeterRow').each(function(){
        var pos = $(this).offset(),
            wY = $(window).scrollTop(),
            wH = $(window).height(),
            oH = $(this).outerHeight();

        cDiv =  $(this).find($('.delimeterListImg'));
        var delta=20;
        if (pos.top >= wY+delta && oH + pos.top <= wY + wH-delta ){
             for (var i = 0; i < cDiv.length; i++) {
                  cDiv[i].style.opacity = '1';  //do styling here
             }
        }else{
             for (var i = 0; i < cDiv.length; i++) {
                  cDiv[i].style.opacity = '0.5';  //do styling here
             }
        }
      });
    }
