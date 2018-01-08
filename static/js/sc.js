function vote(voteButton) {
    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    var $voteDiv = $(voteButton).parent().parent();
    var $data = $voteDiv.data();
    var direction_name = $(voteButton).attr('title');
    var vote_value = null;
    if (direction_name == "upvote") {
        vote_value = 1;
    } else if (direction_name == "downvote") {
        vote_value = -1;
    } else {
        return;
    }

    var doPost = $.post('/vote/', {
        what: $data.whatType,
        what_id: $data.whatId,
        vote_value: vote_value
    });



    doPost.done(function (response) {
        if (response.error == null) {
            var voteDiff = response.voteDiff;
            var $score = null;
            var $upvoteArrow = null;
            var $downArrow = null;
            if ($data.whatType == 'submission') {
                $score = $voteDiv.find("div.score");
                $upvoteArrow = $voteDiv.children("div").children('i.fa.fa-chevron-up');
                $downArrow = $voteDiv.children("div").children('i.fa.fa-chevron-down');
            } else if ($data.whatType == 'comment') {
                var $medaiDiv = $voteDiv.parent().parent();
                var $votes = $medaiDiv.children('div.media-left').children('div.vote').children('div');
                $upvoteArrow = $votes.children('i.fa.fa-chevron-up');
                $downArrow = $votes.children('i.fa.fa-chevron-down');
                $score = $medaiDiv.find('div.media-left:first').find(".score:first");
            }
            // update vote elements

            if (vote_value == -1) {
                if ($upvoteArrow.hasClass("upvoted")) { // remove upvote, if any.
                    $upvoteArrow.removeClass("upvoted")
                }
                if ($downArrow.hasClass("downvoted")) { // Canceled downvote
                    $downArrow.removeClass("downvoted")
                } else {                                // new downvote
                    $downArrow.addClass("downvoted")
                }
            } else if (vote_value == 1) {               // remove downvote
                if ($downArrow.hasClass("downvoted")) {
                    $downArrow.removeClass("downvoted")
                }

                if ($upvoteArrow.hasClass("upvoted")) { // if canceling upvote
                    $upvoteArrow.removeClass("upvoted")
                } else {                                // adding new upvote
                    $upvoteArrow.addClass("upvoted")
                }
            }
            // update score element
            var scoreInt = parseInt($score.text());
            $score.text(scoreInt += voteDiff);

        }
    });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


var newCommentForm = '<form id="commentForm" class="form-horizontal"\
                            action="/post/comment/"\
                            data-parent-type="comment">\
                            <fieldset>\
                            <div class="form-group comment-group">\
                                <div class="col-lg-10">\
                                     <div class="ceFieldWrapper col-9">\
                                        <div contentEditable="true" class="ceField commentContent"></div>\
                                     </div>\
                                </div>\
                            </div>\
                            <div class="form-group">\
                              <div class="row">\
                                <div class="col-3">\
                                    <button type="submit" class="btn btn-primary">Отправить</button>\
                                </div>\
                                <div class="col-3">\
                                    <div align="right" class="addSmilesTree">Смайлы</div>\
                                </div>\
                                <div class"col-3">\
                                    <div class="addCommentImage">Добавить картинку</div>\
                                    <input type="file" name="file" class="displayNone imageFileInput" >\
                                </div>\
                              </div>\
                            </div>\
                        </fieldset>\
                    </form>';

$('a[name="replyButton"]').click(function () {
    var $mediaBody = $(this).parent().parent().parent();
    if ($mediaBody.find('#commentForm').length == 0) {
        $mediaBody.parent().find(".reply-container:first").append(newCommentForm);
        cef = $mediaBody.find(".ceField:first");
        $cefIdCnt = $cefIdCnt+1;
        aci = $mediaBody.find(".addCommentImage:first");
        ifi = $mediaBody.find(".imageFileInput:first");
        cef.attr('id','cef'+ $cefIdCnt);
        ifi.attr('id','ifi'+ $cefIdCnt);
        aci.attr('target-id',ifi.attr('id'));
        aci.click(function(){
            targetId = $(this).attr('target-id');
            $('#'+targetId).css({"display":"block"});
            $(this).css({"display":"none"})
        })

        ast = $mediaBody.find(".addSmilesTree:first");
        ast.click(function(){
            var pos = ast.position();
            $mediaBody.parent().find(".reply-container:first").append($("#smilePanel"));
            $("#smilePanel").css({ top: 200, left: 200});
            $("#smilePanel").show();
        });
        $(".smileImg").attr('target-id',cef.attr('id'));

        var $form = $mediaBody.find('#commentForm');
        $form.data('parent-id', $mediaBody.parent().data().parentId);
        $form.submit(function (event) {
            submitEvent(event, $(this));
        });
    } else {
        $commentForm = $mediaBody.find('#commentForm:first');
        if ($commentForm.attr('style') == null) {
            $commentForm.css('display', 'none')
        } else {
            $commentForm.removeAttr('style')
        }
        $(".addSmilesHolder").append($("#smilePanel"));

        $(".smileImg").attr('target-id','commentContent');

    }

});

$cefIdCnt = 0;

$(document).ready(function(){
    $( ".ytframe" ).each(function( index ) {
      $( this ).height( $( this ).width()*9/16 );
    });
    input = $(".imageFieldWrapper" ).find('input');
    $(".tmpDiv").append(input);
    $(".imageFieldWrapper" ).empty();
    $(".imageFieldWrapper" ).append(input);
});


$(".alert").fadeTo(2000, 500).slideUp(500, function(){
    $(".alert").slideUp(500);
});

$('.addCommentImage').click(function(){
    //restoreSelection(true);
    targetId = $(this).attr('target-id');
    $('#'+targetId).css({"display":"block"});
    $(this).css({"display":"none"})
})
