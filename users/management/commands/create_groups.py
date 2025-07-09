from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Creates default user groups for MindCare'

    def handle(self, *args, **kwargs):
        group_names = ['Admin', 'Therapist', 'Client']
        for name in group_names:
            group, created = Group.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created group: {name}'))
            else:
                self.stdout.write(f'Group already exists: {name}')