from django.db.models import Q
from repoGenerico.views_base import BaseListQueryView
from academy.models import Lesson
from academy.serializers import LessonSerializer
class CatalogQuery(BaseListQueryView):
    model=Lesson
    serializer_class=LessonSerializer
    def apply_search(self,queryset,search):
        return queryset.filter(Q(title__icontains=search)|Q(concept__icontains=search)) if search else queryset
