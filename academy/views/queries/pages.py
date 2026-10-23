from django.views.generic import TemplateView
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_sameorigin
from academy.catalog import LESSONS, UNITS, get_lesson
from academy.mixins import CourseContextMixin

class HomeView(CourseContextMixin, TemplateView):
    template_name = 'academy/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '').strip()[:200]
        selected = self.request.GET.get('unit', '')
        lessons = [lesson for lesson in LESSONS if
            query.casefold() in (lesson['title'] + ' ' + lesson['concept'] + ' ' + ' '.join(lesson['theory'])).casefold()
            and (not selected or str(lesson['unit']) == selected)]
        context.update(lessons=lessons, q=query, units=UNITS, selected_unit=selected)
        return context

class LessonView(CourseContextMixin, TemplateView):
    template_name = 'academy/lesson.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = get_lesson(kwargs['pk'])
        if lesson is None:
            raise Http404
        context.update(lesson=lesson, unit=UNITS[lesson['unit'] - 1],
            previous=LESSONS[lesson['position'] - 2]['id'] if lesson['position'] > 1 else None,
            next=LESSONS[lesson['position']]['id'] if lesson['position'] < len(LESSONS) else None,
            chapter_lessons=[item for item in LESSONS if item['unit'] == lesson['unit']])
        return context


@method_decorator(xframe_options_sameorigin, name='dispatch')
class GameView(TemplateView):
    template_name = 'academy/game.html'


class StoryView(CourseContextMixin, TemplateView):
    """Lectura continua, pública y sin estado de autenticación."""
    template_name = "academy/story.html"
