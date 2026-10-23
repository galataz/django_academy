from django.core.management.base import BaseCommand
from django.db import transaction
from academy.models import Lesson
from academy.catalog import LESSONS
class Command(BaseCommand):
    help='Sincroniza catálogo público desde contenido versionado.'
    @transaction.atomic
    def handle(self,*args,**options):
        for item in LESSONS:
            Lesson.objects.update_or_create(number=item['id'],defaults={'title':item['title'],'concept':item['concept'],'source_path':''})
        Lesson.objects.exclude(number__in=[x['id'] for x in LESSONS]).delete()
        self.stdout.write(self.style.SUCCESS(f'{len(LESSONS)} temas sincronizados.'))
