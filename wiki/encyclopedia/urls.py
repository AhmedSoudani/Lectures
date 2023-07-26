from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search_result", views.search_result, name="search_result"),
    path("<str:title>", views.wiki_page_view, name="wiki_page"),
    
]
