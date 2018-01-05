from django.core.management.base import BaseCommand

from users.models import ScUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        u = ScUser.objects.first()
        tests = [1234, 100000, 299792458, 759878, 123, 12232, 12321, 90]
        for test in tests:
            print("%d %s" % (test, u.getShortKarmaVal(test)))
