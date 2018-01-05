# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponseBadRequest, Http404, \
    HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.template import RequestContext
from django.template.defaulttags import register

from sc.forms import SubmissionForm
from sc.models import Submission, Comment, Vote, CreativeType
from sc.utils.helpers import post_only
from users.models import ScUser


@register.filter
def get_item(dictionary, key):  # pragma: no cover
    """
    Needed because there's no built in .get in django templates
    when working with dictionaries.

    :param dictionary: python dictionary
    :param key: valid dictionary key type
    :return: value of that key or None
    """
    return dictionary.get(key)


def comments(request, thread_id=None):
    """
    Handles comment view when user opens the thread.
    On top of serving all comments in the thread it will
    also return all votes user made in that thread
    so that we can easily update comments in template
    and display via css whether user voted or not.

    :param thread_id: Thread ID as it's stored in database
    :type thread_id: int
    """

    this_submission = get_object_or_404(Submission, id=thread_id)
    this_submission.viewCnt += 1
    this_submission.save()

    thread_comments = Comment.objects.filter(submission=this_submission)

    if request.user.is_authenticated():
        try:
            reddit_user = ScUser.objects.get(user=request.user)
        except ScUser.DoesNotExist:
            reddit_user = None
    else:
        reddit_user = None

    sub_vote_value = None
    comment_votes = {}

    if reddit_user:
        try:
            vote = Vote.objects.get(
                vote_object_type=this_submission.get_content_type(),
                vote_object_id=this_submission.id,
                user=reddit_user)
            sub_vote_value = vote.value
        except Vote.DoesNotExist:
            pass

        try:
            user_thread_votes = Vote.objects.filter(user=reddit_user,
                                                    submission=this_submission)

            for vote in user_thread_votes:
                comment_votes[vote.vote_object.id] = vote.value
        except:
            pass

    flgPower = False

    if this_submission.tp == Submission.TP_CREATIVE:
        linkPrefix = '/creative/'
    elif this_submission.tp == Submission.TP_CHALLENGE:
        linkPrefix = '/power/creative/'
        flgPower = True
    elif this_submission.tp == Submission.TP_FAQ:
        linkPrefix = '/faq/'

    canEdit = False
    canDelete = False
    canDeleteComments = False

    if this_submission.author.user == request.user:
        canEdit = True
        canDelete = True

    if is_moderator(request.user):
        canDeleteComments = True
        canDelete = True

    vote_s_val = 0
    try:
        voteS = Vote.objects.get(
                vote_object_type=this_submission.get_content_type(),
                vote_object_id=this_submission.id,
                user=ScUser.objects.get(user=request.user))
        vote_s_val = voteS.value
    except Vote.DoesNotExist:
        pass

    return render(request, 'public/comments.html',
                  {'submission': this_submission,
                   'linkPrefix': linkPrefix,
                   'flgPower': flgPower,
                   'canDelete': canDelete,
                   'canDeleteComments': canDeleteComments,
                   'canEdit': canEdit,
                   'comments': thread_comments,
                   'comment_votes': comment_votes,
                   'sub_vote': sub_vote_value,
                   'vote_s_val':vote_s_val})


@login_required
def delete(request, thread_id=None):
    """
    Handles comment view when user opens the thread.
    On top of serving all comments in the thread it will
    also return all votes user made in that thread
    so that we can easily update comments in template
    and display via css whether user voted or not.

    :param thread_id: Thread ID as it's stored in database
    :type thread_id: int
    """

    this_submission = get_object_or_404(Submission, id=thread_id)
    if not (is_moderator(request.user) or request.user == this_submission.author.user):
        return HttpResponseRedirect('/permission/denied/')

    # удаляем комментарии
    Comment.objects.filter(submission=this_submission).delete()
    Vote.objects.filter(submission=this_submission).delete()
    this_submission.delete()
    return HttpResponseRedirect('/creative/')


"""
Рекурентное удаление комментариев с потомками
"""


def deleteCommentWithChildren(comment):
    for com in Comment.objects.filter(parent=comment):
        deleteCommentWithChildren(com)

    comment.submission.comment_count = comment.submission.comment_count - 1
    comment.submission.save()
    comment.delete()


# удалить комментарий по его id (и его потомков)
@login_required
def deleteComment(request, thread_id=None):
    if not is_moderator(request.user):
        return HttpResponseRedirect('/permission/denied/')
    """
    Handles comment view when user opens the thread.
    On top of serving all comments in the thread it will
    also return all votes user made in that thread
    so that we can easily update comments in template
    and display via css whether user voted or not.

    :param thread_id: Thread ID as it's stored in database
    :type thread_id: int
    """

    this_comment = get_object_or_404(Comment, id=thread_id)
    deleteCommentWithChildren(this_comment)

    return HttpResponseRedirect('/creative/')


@login_required
def edit(request, thread_id=None):
    """
      Handles new submission.. submission.
      """
    this_submission = get_object_or_404(Submission, id=thread_id)
    if request.user != this_submission.author.user:
        return HttpResponseRedirect('/permission/denied/')

    url = this_submission.url
    if this_submission.link_type == Submission.LINK_TYPE_FLICKR:
        url = '<img src="' + this_submission.url + '">'
    elif this_submission.link_type == Submission.LINK_TYPE_SOUNDCLOUND:
        url = 'src="' + this_submission.url + '">'
    elif this_submission.link_type == Submission.LINK_TYPE_YOUTUBE:
        url = this_submission.url.replace("embed/", "watch?v=")

    submission_form = SubmissionForm(instance=this_submission, initial={'ctp': this_submission.getCtp(), 'url': url})

    if request.method == 'POST':
        submission_form = SubmissionForm(request.POST)
        if submission_form.is_valid():
            submission_form.save(commit=False)
            this_submission.link_type = submission_form.link_type
            this_submission.generate_html()
            this_submission.title = submission_form.cleaned_data["title"]
            this_submission.save()

            this_submission.creativeType.clear()
            for tp in submission_form.cleaned_data['ctp']:
                #   print(tp)
                this_submission.creativeType.add(tp)

            return redirect('/comments/{}'.format(this_submission.id))

    return render(request, 'public/submit.html', {'form': submission_form, 'caption': 'Редактирование'})
    # return render(request, 'public/submit.html', {'form': None})


@post_only
def post_comment(request):
    if not request.user.is_authenticated():
        return JsonResponse({'msg': "You need to log in to post new comments."})

    parent_type = request.POST.get('parentType', None)
    parent_id = request.POST.get('parentId', None)
    raw_comment = request.POST.get('commentContent', None)

    if not all([parent_id, parent_type]) or \
            parent_type not in ['comment', 'submission'] or \
        not parent_id.isdigit():
        return HttpResponseBadRequest()

    if not raw_comment:
        return JsonResponse({'msg': "You have to write something."})
    author = ScUser.objects.get(user=request.user)
    parent_object = None
    try:  # try and get comment or submission we're voting on
        if parent_type == 'comment':
            parent_object = Comment.objects.get(id=parent_id)
        elif parent_type == 'submission':
            parent_object = Submission.objects.get(id=parent_id)

    except (Comment.DoesNotExist, Submission.DoesNotExist):
        return HttpResponseBadRequest()

    comment = Comment.create(author=author,
                             raw_comment=raw_comment,
                             parent=parent_object)

    comment.save()
    return JsonResponse({'msg': "Your comment has been posted."})


@post_only
def vote(request):
    # The type of object we're voting on, can be 'submission' or 'comment'
    vote_object_type = request.POST.get('what', None)

    # The ID of that object as it's stored in the database, positive int
    vote_object_id = request.POST.get('what_id', None)

    # The value of the vote we're writing to that object, -1 or 1
    # Passing the same value twice will cancel the vote i.e. set it to 0
    new_vote_value = request.POST.get('vote_value', None)

    # By how much we'll change the score, used to modify score on the fly
    # client side by the javascript instead of waiting for a refresh.
    vote_diff = 0

    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    else:
        user = ScUser.objects.get(user=request.user)

    try:  # If the vote value isn't an integer that's equal to -1 or 1
        # the request is bad and we can not continue.
        new_vote_value = int(new_vote_value)

        if new_vote_value not in [-1, 1]:
            raise ValueError("Wrong value for the vote!")

    except (ValueError, TypeError):
        return HttpResponseBadRequest()

    # if one of the objects is None, 0 or some other bool(value) == False value
    # or if the object type isn't 'comment' or 'submission' it's a bad request
    if not all([vote_object_type, vote_object_id, new_vote_value]) or \
            vote_object_type not in ['comment', 'submission']:
        return HttpResponseBadRequest()

    # Try and get the actual object we're voting on.
    try:
        if vote_object_type == "comment":
            vote_object = Comment.objects.get(id=vote_object_id)

        elif vote_object_type == "submission":
            vote_object = Submission.objects.get(id=vote_object_id)
        else:
            return HttpResponseBadRequest()  # should never happen

    except (Comment.DoesNotExist, Submission.DoesNotExist):
        return HttpResponseBadRequest()

    # Try and get the existing vote for this object, if it exists.
    try:
        vote = Vote.objects.get(vote_object_type=vote_object.get_content_type(),
                                vote_object_id=vote_object.id,
                                user=user)

    except Vote.DoesNotExist:
        # Create a new vote and that's it.
        vote = Vote.create(user=user,
                           vote_object=vote_object,
                           vote_value=new_vote_value)
        vote.save()
        vote_diff = new_vote_value
        return JsonResponse({'error': None,
                             'voteDiff': vote_diff})

    # User already voted on this item, this means the vote is either
    # being canceled (same value) or changed (different new_vote_value)
    if vote.value == new_vote_value:
        # canceling vote
        vote_diff = vote.cancel_vote()
        if not vote_diff:
            return HttpResponseBadRequest(
                'Something went wrong while canceling the vote')
    else:
        # changing vote
        vote_diff = vote.change_vote(new_vote_value)
        if not vote_diff:
            return HttpResponseBadRequest(
                'Wrong values for old/new vote combination')

    return JsonResponse({'error': None,
                         'voteDiff': vote_diff})


@login_required
def submit(request):
    """
    Handles new submission.. submission.
    """
    submission_form = SubmissionForm()

    if request.method == 'POST':
        submission_form = SubmissionForm(request.POST)
        if submission_form.is_valid():
            submission = submission_form.save(commit=False)
            submission.link_type = submission_form.link_type
            submission.tp = Submission.TP_CREATIVE
            submission.generate_html()
            user = User.objects.get(username=request.user)
            redditUser = ScUser.objects.get(user=user)
            submission.author = redditUser
            submission.author_name = user.username
            submission.save()
            submission.creativeType.clear()
            for tp in submission_form.cleaned_data['ctp']:
                #   print(tp)
                submission.creativeType.add(tp)

            return redirect('/comments/{}'.format(submission.id))

    return render(request, 'public/submit.html', {'form': submission_form, 'caption': 'Добавить пост'})


def permissionDenied(request):
    return render(request, 'permissionDenied.html', {})


@login_required
def submitFAQ(request):
    if not is_moderator(request.user):
        return HttpResponseRedirect('/permission/denied/')
    """
    Handles new submission.. submission.
    """
    submission_form = SubmissionForm()

    if request.method == 'POST':
        submission_form = SubmissionForm(request.POST)
        if submission_form.is_valid():
            submission = submission_form.save(commit=False)
            submission.link_type = submission_form.link_type
            submission.tp = Submission.TP_FAQ
            submission.generate_html()
            user = User.objects.get(username=request.user)
            redditUser = ScUser.objects.get(user=user)
            submission.author = redditUser
            submission.author_name = user.username
            submission.save()
            submission.creativeType.clear()
            for tp in submission_form.cleaned_data['ctp']:
                #   print(tp)
                submission.creativeType.add(tp)

            return redirect('/comments/{}'.format(submission.id))

    return render(request, 'public/submit.html', {'form': submission_form, 'caption': 'Добавить'})


@login_required
def submitPower(request):
    """
    Handles new submission.. submission.
    """
    submission_form = SubmissionForm()

    if request.method == 'POST':
        submission_form = SubmissionForm(request.POST)
        if submission_form.is_valid():
            submission = submission_form.save(commit=False)
            submission.link_type = submission_form.link_type
            submission.tp = Submission.TP_CHALLENGE
            submission.generate_html()
            user = User.objects.get(username=request.user)
            redditUser = ScUser.objects.get(user=user)
            submission.author = redditUser
            submission.author_name = user.username
            submission.save()
            submission.creativeType.clear()
            for tp in submission_form.cleaned_data['ctp']:
                #   print(tp)
                submission.creativeType.add(tp)

            return redirect('/comments/{}'.format(submission.id))

    return render(request, 'public/submit.html', {'form': submission_form, 'caption': 'Добавить', 'flgPower': True})


def getCreativeByType(request, ct, sctp, flgNew=False,username=""):
    template = 'public/creative_list.html'
    canAdd = request.user.is_authenticated
    canEdit = False
    canDelete = is_moderator(request.user)

    if sctp == Submission.TP_CHALLENGE:
        titleText = 'Боевой Креатив'
        titleLink = '/power/creative'
        createLink = '/submit/power/'
        prefix = '/power/creative'


    elif sctp == Submission.TP_CREATIVE:
        titleText = 'Креатив'
        titleLink = '/creative'
        createLink = '/submit/'
        prefix = '/creative'

    elif sctp == Submission.TP_FAQ:
        titleText = 'О проекте'
        titleLink = '/faq/'
        createLink = '/submit/faq/'
        prefix = '/faq'
        template = 'public/faq_list.html'
        canAdd = is_moderator(request.user)

    if sctp == Submission.TP_USER_CREATIVE:
        canEdit = username == request.user.username
        canDelete = canEdit
        titleText = username
        titleLink = '/user/' + username
        createLink = '/submit/'
        prefix = '/user/' + username + '/creative'

        if ct != '':
            all_submissions = Submission.objects.filter(
                author=ScUser.objects.get(user=User.objects.get(username=username)),
                creativeType=CreativeType.objects.get(name=ct)
            )
        else:
            all_submissions = Submission.objects.filter(
                author=ScUser.objects.get(user=User.objects.get(username=username)),
            )
    else:
        if ct != '':
            all_submissions = Submission.objects.filter(
                tp=sctp,
                creativeType=CreativeType.objects.get(name=ct)
            )
        else:
            all_submissions = Submission.objects.filter(tp=sctp)

    common_prefix = prefix
    new_prefix = prefix+'/new'

    if flgNew:
        prefix = new_prefix
        all_submissions = all_submissions.order_by('-timestamp').all()
    else:
        all_submissions = all_submissions.order_by('-score').all()
    """
      Serves frontpage and all additional submission listings
      with maximum of 25 submissions per page.
      """
    # TODO: Serve user votes on submissions too.

    paginator = Paginator(all_submissions, 7)

    page = request.GET.get('page', 1)
    try:
        submissions = paginator.page(page)
    except PageNotAnInteger:
        raise Http404
    except EmptyPage:
        submissions = paginator.page(paginator.num_pages)

    submission_votes = {}

    if request.user.is_authenticated():
        for submission in submissions:
            try:
                vote = Vote.objects.get(
                    vote_object_type=submission.get_content_type(),
                    vote_object_id=submission.id,
                    user=ScUser.objects.get(user=request.user))
                submission_votes[submission.id] = vote.value
            except Vote.DoesNotExist:
                pass

    return render(request, template, {
        'submissions': submissions,
        'titleText': titleText,
        'titleLink': titleLink,
        'createLink': createLink,
        'prefix': prefix,
        'canDelete': canDelete,
        'canEdit': canEdit,
        'canAdd': canAdd,
        'ct': ct,
        'flgNew':flgNew,
        'new_prefix':new_prefix,
        'common_prefix':common_prefix,
        'submission_votes': submission_votes
    })



def frontPage(request):
    return render(request, 'public/front_page.html', {'flgMainPage': True})


def ehandler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def ehandler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response


def is_moderator(user):
    return user.groups.filter(name='moderators').exists()


def powerCreative(request):
    return getCreativeByType(request, '', Submission.TP_CHALLENGE)


def designP(request):
    return getCreativeByType(request, 'Дизайн', Submission.TP_CHALLENGE)


def conceptionP(request):
    return getCreativeByType(request, 'Концепция', Submission.TP_CHALLENGE)


def storyP(request):
    return getCreativeByType(request, 'Сюжет', Submission.TP_CHALLENGE)


def inventionP(request):
    return getCreativeByType(request, 'Изобретения', Submission.TP_CHALLENGE)


def musicP(request):
    return getCreativeByType(request, 'Музыка', Submission.TP_CHALLENGE)


def videoP(request):
    return getCreativeByType(request, 'Видео', Submission.TP_CHALLENGE)


def creative(request):
    return getCreativeByType(request, '', Submission.TP_CREATIVE)


def design(request):
    return getCreativeByType(request, 'Дизайн', Submission.TP_CREATIVE)


def conception(request):
    return getCreativeByType(request, 'Концепция', Submission.TP_CREATIVE)


def story(request):
    return getCreativeByType(request, 'Сюжет', Submission.TP_CREATIVE)


def invention(request):
    return getCreativeByType(request, 'Изобретения', Submission.TP_CREATIVE)


def music(request):
    return getCreativeByType(request, 'Музыка', Submission.TP_CREATIVE)


def video(request):
    return getCreativeByType(request, 'Видео', Submission.TP_CREATIVE)


def faq(request):
    return getCreativeByType(request, '', Submission.TP_FAQ)



def newPowerCreative(request):
    return getCreativeByType(request, '', Submission.TP_CHALLENGE,True)


def newDesignP(request):
    return getCreativeByType(request, 'Дизайн', Submission.TP_CHALLENGE,True)


def newConceptionP(request):
    return getCreativeByType(request, 'Концепция', Submission.TP_CHALLENGE,True)


def newStoryP(request):
    return getCreativeByType(request, 'Сюжет', Submission.TP_CHALLENGE,True)


def newInventionP(request):
    return getCreativeByType(request, 'Изобретения', Submission.TP_CHALLENGE,True)


def newMusicP(request):
    return getCreativeByType(request, 'Музыка', Submission.TP_CHALLENGE,True)


def newVideoP(request):
    return getCreativeByType(request, 'Видео', Submission.TP_CHALLENGE,True)


def newCreative(request):
    return getCreativeByType(request, '', Submission.TP_CREATIVE,True)


def newDesign(request):
    return getCreativeByType(request, 'Дизайн', Submission.TP_CREATIVE,True)


def newConception(request):
    return getCreativeByType(request, 'Концепция', Submission.TP_CREATIVE,True)


def newStory(request):
    return getCreativeByType(request, 'Сюжет', Submission.TP_CREATIVE,True)


def newInvention(request):
    return getCreativeByType(request, 'Изобретения', Submission.TP_CREATIVE,True)


def newMusic(request):
    return getCreativeByType(request, 'Музыка', Submission.TP_CREATIVE,True)


def newVideo(request):
    return getCreativeByType(request, 'Видео', Submission.TP_CREATIVE,True)

