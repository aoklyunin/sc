from django.contrib import admin

# Register your models here.
from sc.admin import SubmissionInline
from users.models import ScUser


class ScUserAdmin(admin.ModelAdmin):
    inlines = [
        SubmissionInline,
    ]

admin.site.register(ScUser, ScUserAdmin)
