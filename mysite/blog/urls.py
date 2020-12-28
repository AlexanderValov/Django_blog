from django.urls import path, include
from . import views

app_name = 'blog'

urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail, name='post_detail'),
    path('new_post/', views.add_post, name='add_post'),
    path('search/', views.post_search, name='post_search'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/update_post/', views.update_post, name='update_post'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/delete_post/', views.delete_post, name='delete_post'),
]
