from academy.catalog import LESSONS, UNITS, STORY, NARRATIVE, JOURNEY, JOURNEY_ORDER
class CourseContextMixin:
    """Composición cooperativa: añade navegación sin duplicar TemplateView."""
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['story_chapters']=STORY
        context['narrative_book']=NARRATIVE
        context['total']=len(LESSONS)
        context['course_order']=JOURNEY_ORDER
        context['journey_stages']=JOURNEY
        context['journey_progress']=[{'slug': s['slug'], 'lessons': s['lessons'], 'title': s['title']} for s in JOURNEY]
        context['unit_count']=len(UNITS)
        return context
