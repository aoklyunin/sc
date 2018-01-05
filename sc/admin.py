# -*- coding: utf-8 -*-

from django.contrib import admin
from sc.models import Submission, Comment, Vote, CreativeType


# Register your models here.
class SubmissionInline(admin.TabularInline):
    model = Submission
    max_num = 10

class CommentsInline(admin.StackedInline):
    model = Comment
    max_num = 10

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'author','tp')
    inlines = [CommentsInline]

admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(CreativeType)
