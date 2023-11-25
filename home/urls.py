from django.urls import path
from .views import home, todo_post, get_todo, patch_todo, Todo_view

urlpatterns = [
    path('', home, name='home'),
    path('todo_post/', todo_post, name='todo_post'),
    path('get_todo/', get_todo, name='get_todo'),
    path('patch-todo/', patch_todo, name='patch-todo'),

    # for class based
    path('todo/', Todo_view.as_view())

]
