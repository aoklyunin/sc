# -*- coding: utf-8 -*-


import mistune
import re
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey
from sc_main.utils.model_utils import ContentTypeAware, MttpContentTypeAware


class CreativeType(models.Model):
    TP_MENU_ITEM = 0
    TP_MENU_HEADER = 1

    name = models.CharField(max_length=100)
    link = models.CharField(max_length=100, blank=True)
    tp = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Submission(ContentTypeAware):
    TP_CREATIVE = 0
    TP_CHALLENGE = 1
    TP_FAQ = 2
    TP_USER_CREATIVE = 3

    LINK_TYPE_NOT_PROCESSED = 0
    LINK_TYPE_FLICKR = 1
    LINK_TYPE_YOUTUBE = 2
    LINK_TYPE_SOUNDCLOUND = 3

    creativeType = models.ManyToManyField(CreativeType, blank=True)
    author_name = models.CharField(null=False, max_length=12)
    author = models.ForeignKey('users.ScUser')
    title = models.CharField(max_length=250)
    url = models.CharField(null=True, blank=True, max_length=1000)
    text = models.TextField(max_length=5000, blank=True)
    text_html = models.TextField(blank=True)
    ups = models.IntegerField(default=0)
    downs = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=timezone.now())
    comment_count = models.IntegerField(default=0)
    tp = models.IntegerField(default=TP_CREATIVE)
    link_type = models.IntegerField(default=-1)
    link_width = models.IntegerField(default=0)
    link_height = models.IntegerField(default=0)
    viewCnt = models.IntegerField(default=0)
    regard = models.IntegerField(default=0)
    stoDate = models.DateTimeField(default=timezone.now())

    def processUrl(self, url):
        # flickr
        match = re.search(r'<img src="[\'"]?([^\'" >]+)staticflickr([^\'" >]+)"', self.url)
        if match:
            url = match.group(0)[10:-1]
            link_type = Submission.LINK_TYPE_FLICKR
        else:
            # soundcloud
            match = re.search(r'src="https:\/\/w.soundcloud.com\/[\'"]?([^\'" >]+)"', self.url)
            if match:
                self.url = match.group(0)[5:-1]
                self.link_type = Submission.LINK_TYPE_SOUNDCLOUND
            else:
                # youtube
                match = re.search(r'[\'"]?([^\'" >]+)youtube([^\'" >]+)', self.url)
                if match:
                    self.url = match.group(0).replace("watch?v=", "embed/")
                    self.link_type = Submission.LINK_TYPE_YOUTUBE
                else:
                    match = re.search(r'[\'"]?([^\'" >]+).([^\'" >]+)', self.url)
                    if match:
                        self.link_type = Submission.LINK_TYPE_NOT_PROCESSED
                        self.url = match.group(0)
                    else:
                        pass
                        # raise ValidationError("Не удалось расшифровать ссылку")

    def getCtp(self):
        lst = []
        for sch in self.creativeType.all():
            lst.append(str(sch.pk))
        return lst

    def generate_html(self):
        if self.text:
            html = mistune.markdown(self.text)
            self.text_html = html

    @property
    def linked_url(self):
        if self.url:
            return "{}".format(self.url)
        else:
            return "/comments/{}".format(self.id)

    @property
    def comments_url(self):
        return '/comments/{}'.format(self.id)

    def __unicode__(self):
        return "<Submission:{}>".format(self.id)


class Comment(MttpContentTypeAware):
    author_name = models.CharField(null=False, max_length=12)
    author = models.ForeignKey('users.ScUser')
    submission = models.ForeignKey(Submission)
    parent = TreeForeignKey('self', related_name='children',
                            null=True, blank=True, db_index=True)
    timestamp = models.DateTimeField(default=timezone.now())
    ups = models.IntegerField(default=0)
    downs = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    raw_comment = models.TextField(blank=True)
    html_comment = models.TextField(blank=True)
    markedBySubmissionOwner = models.BooleanField(default=False)
    url = models.CharField(null=True, blank=True, max_length=1000)
    ltp = models.IntegerField(default=0)

    class MPTTMeta:
        order_insertion_by = ['-score']

    @classmethod
    def create(cls, author, raw_comment, parent, ltp, link):
        """
        Create a new comment instance. If the parent is submisison
        update comment_count field and save it.
        If parent is comment post it as child comment
        :param author: RedditUser instance
        :type author: RedditUser
        :param raw_comment: Raw comment text
        :type raw_comment: str
        :param parent: Comment or Submission that this comment is child of
        :type parent: Comment | Submission
        :return: New Comment instance
        :rtype: Comment
        """

        html_comment = mistune.markdown(raw_comment)
        # todo: any exceptions possible?
        comment = cls(author=author,
                      author_name=author.user.username,
                      raw_comment=raw_comment,
                      html_comment=html_comment,
                      ltp=ltp,
                      url=link)

        if isinstance(parent, Submission):
            submission = parent
            comment.submission = submission
        elif isinstance(parent, Comment):
            submission = parent.submission
            comment.submission = submission
            comment.parent = parent
        else:
            return
        submission.comment_count += 1
        submission.save()

        return comment

    def __unicode__(self):
        return "<Comment:{}>".format(self.id)


class Vote(models.Model):
    user = models.ForeignKey('users.ScUser')
    submission = models.ForeignKey(Submission)
    vote_object_type = models.ForeignKey(ContentType)
    vote_object_id = models.PositiveIntegerField()
    vote_object = GenericForeignKey('vote_object_type', 'vote_object_id')
    value = models.IntegerField(default=0)

    @classmethod
    def create(cls, user, vote_object, vote_value):
        """
        Create a new vote object and return it.
        It will also update the ups/downs/score fields in the
        vote_object instance and save it.

        :param user: RedditUser instance
        :type user: RedditUser
        :param vote_object: Instance of the object the vote is cast on
        :type vote_object: Comment | Submission
        :param vote_value: Value of the vote
        :type vote_value: int
        :return: new Vote instance
        :rtype: Vote
        """

        if isinstance(vote_object, Submission):
            submission = vote_object
        else:
            submission = vote_object.submission

        if submission.tp == Submission.TP_CREATIVE:
            vote_object.author.creativeKarma += vote_value

        if submission.tp == Submission.TP_CHALLENGE:
            vote_object.author.powerKarma += vote_value

        vote = cls(user=user,
                   vote_object=vote_object,
                   value=vote_value)

        vote.submission = submission
        # the value for new vote will never be 0
        # that can happen only when removing up/down vote.
        vote_object.score += vote_value
        if vote_value == 1:
            vote_object.ups += 1
        elif vote_value == -1:
            vote_object.downs += 1

        vote_object.save()
        vote_object.author.save()

        return vote

    def change_vote(self, new_vote_value):
        if self.value == -1 and new_vote_value == 1:  # down to up
            vote_diff = 2
            self.vote_object.score += 2
            self.vote_object.ups += 1
            self.vote_object.downs -= 1
        elif self.value == 1 and new_vote_value == -1:  # up to down
            vote_diff = -2
            self.vote_object.score -= 2
            self.vote_object.ups -= 1
            self.vote_object.downs += 1
        elif self.value == 0 and new_vote_value == 1:  # canceled vote to up
            vote_diff = 1
            self.vote_object.ups += 1
            self.vote_object.score += 1
        elif self.value == 0 and new_vote_value == -1:  # canceled vote to down
            vote_diff = -1
            self.vote_object.downs += 1
            self.vote_object.score -= 1
        else:
            return None

        if isinstance(self.vote_object, Submission):
            submission = self.vote_object
        else:
            submission = self.vote_object.submission

        if submission.tp == Submission.TP_CREATIVE:
            self.vote_object.author.creativeKarma += vote_diff

        if submission.tp == Submission.TP_CHALLENGE:
            self.vote_object.author.powerKarma += vote_diff

        self.value = new_vote_value
        self.vote_object.save()
        self.vote_object.author.save()
        self.save()

        return vote_diff

    def cancel_vote(self):
        if self.value == 1:
            vote_diff = -1
            self.vote_object.ups -= 1
            self.vote_object.score -= 1
        elif self.value == -1:
            vote_diff = 1
            self.vote_object.downs -= 1
            self.vote_object.score += 1
        else:
            return None

        if isinstance(self.vote_object, Submission):
            submission = self.vote_object
        else:
            submission = self.vote_object.submission

        if submission.tp == Submission.TP_CREATIVE:
            self.vote_object.author.creativeKarma += vote_diff

        if submission.tp == Submission.TP_CHALLENGE:
            self.vote_object.author.powerKarma += vote_diff

        self.value = 0
        self.save()
        self.vote_object.save()
        self.vote_object.author.save()
        return vote_diff


class Analytic(models.Model):
    user = models.ForeignKey('users.ScUser', blank=True)
    val1 = models.IntegerField(default=0)
    val2 = models.CharField(default=0, max_length=10000)
    val3 = models.CharField(default=0, max_length=10000)
    dt = models.DateTimeField(default=timezone.now())
