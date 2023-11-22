from django.urls import path
from .views import home, todo_post

urlpatterns = [
    path('', home, name='home'),
    path('todo_post/', todo_post, name='todo_post')

]
