from academy.catalog import LESSONS, UNITS, STORY, NARRATIVE
class CourseContextMixin:
    """Composición cooperativa: añade navegación sin duplicar TemplateView."""
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['story_chapters']=STORY
        context['narrative_book']=NARRATIVE
        context['total']=len(LESSONS)
        context['course_order']=[lesson['id'] for lesson in LESSONS]
        context['unit_count']=len(UNITS)
        return context
