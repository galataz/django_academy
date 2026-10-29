from django.views.generic import TemplateView
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_sameorigin
from academy.catalog import LESSONS, UNITS, get_lesson, JOURNEY, get_stage, stage_for_lesson, ACCEPTANCE
from academy.mixins import CourseContextMixin

class HomeView(CourseContextMixin, TemplateView):
    template_name = 'academy/home.html'
    def get_template_names(self):
        # Mantener enlaces guardados /?q= y /?unit= del catálogo anterior.
        if 'q' in self.request.GET or 'unit' in self.request.GET:
            return ['academy/catalog.html']
        return [self.template_name]
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '').strip()[:200]
        selected = self.request.GET.get('unit', '')
        lessons = [lesson for lesson in LESSONS if
            query.casefold() in (lesson['title'] + ' ' + lesson['concept'] + ' ' + ' '.join(lesson['theory'])).casefold()
            and (not selected or str(lesson['unit']) == selected)]
        context.update(lessons=lessons, q=query, units=UNITS, selected_unit=selected)
        return context

class CatalogView(HomeView):
    template_name = 'academy/catalog.html'

class StageView(CourseContextMixin, TemplateView):
    template_name = 'academy/stage.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stage = get_stage(kwargs['slug'])
        if stage is None:
            raise Http404
        index = JOURNEY.index(stage)
        context.update(stage=stage, acceptance=ACCEPTANCE if index == 0 else [],
            previous_stage=JOURNEY[index - 1] if index else None,
            next_stage=JOURNEY[index + 1] if index + 1 < len(JOURNEY) else None)
        return context

class LessonView(CourseContextMixin, TemplateView):
    template_name = 'academy/lesson.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = get_lesson(kwargs['pk'])
        if lesson is None:
            raise Http404
        stage = stage_for_lesson(lesson['id'])
        index = stage['lessons'].index(lesson['id'])
        context.update(lesson=lesson, unit=UNITS[lesson['unit'] - 1], stage=stage,
            previous=stage['lessons'][index - 1] if index is not None and index > 0 else None,
            next=stage['lessons'][index + 1] if index is not None and index + 1 < len(stage['lessons']) else None,
            chapter_lessons=stage['topics'])
        return context


@method_decorator(xframe_options_sameorigin, name='dispatch')
class GameView(TemplateView):
    template_name = 'academy/game.html'


class StoryView(CourseContextMixin, TemplateView):
    """Lectura continua, pública y sin estado de autenticación."""
    template_name = "academy/story.html"
