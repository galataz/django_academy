from django.urls import path
from academy.views.queries.pages import HomeView,LessonView,GameView,StoryView
from academy.views.queries.catalog import CatalogQuery
from academy.views.commands.convert import ConvertTemperatureCommand
from config.health import health,ready
urlpatterns=[path('historia/',StoryView.as_view(),name='story'),path('laboratorio/',GameView.as_view(),name='game'),path('',HomeView.as_view(),name='home'),path('tema/<int:pk>/',LessonView.as_view(),name='lesson'),path('api/catalogo/',CatalogQuery.as_view()),path('api/laboratorio/temperatura/',ConvertTemperatureCommand.as_view()),path('health/',health),path('ready/',ready)]
