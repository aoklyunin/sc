from random import choice, randint
from string import ascii_letters as letters

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from sc.models import Comment
from sc.models import Submission
from sc_main import settings
from sc_main.settings import production
from users.models import ScUser


class Command(BaseCommand):

    def handle(self, *args, **options):
        print(production.ALLOWED_HOSTS)
