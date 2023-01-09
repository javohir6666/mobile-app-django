from django.urls import path
from api import views
urlpatterns = [
    path('', views.index, name='admin_home'),
    path('user-list/', views.user_list, name='user_list'),
    path('user-create/', views.user_create, name='user_create'),
    path('search/', views.user_search, name='user_search'),
    path('todo-search/', views.todo_search, name='todo_search'),
    path('todo-list/', views.todo_list, name='todo_list'),
    path('todo-create/', views.todo_create, name='todo_create'),
    path('todo-edit/<int:pk>', views.todo_edit, name='todo_edit'),
    path('todo-delete/<int:pk>', views.todo_delete, name='todo_delete'),

]