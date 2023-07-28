from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search_result", views.search_result, name="search_result"),
    path("random_page", views.random_page, name="random_page"),
    path("new_page", views.new_page, name="new_page"),
    path("edit_page/<str:title>", views.edit_page, name="edit_page"),
    path("save_page", views.save_page, name="save_page"),
    path("<str:title>", views.wiki_page_view, name="wiki_page"),
]
