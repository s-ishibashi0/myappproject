from django.urls import path
from . import views
from .views import SearchView


app_name = 'myapp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('post/', views.CreateMyappView.as_view(), name='post'),
    path('post_done/', views.PostSuccessView.as_view(), name='post_done'),
    path('myapp/<int:category>/', views.CategoryView.as_view(), name='myapp_cat'),
    path('myapp-detail/<int:pk>/', views.DetailView.as_view(), name='myapp_detail'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
     path('search/', SearchView.as_view(), name='search'),  # クラスベースビューを指定
]
