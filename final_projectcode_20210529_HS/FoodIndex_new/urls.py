from django.contrib import admin
from django.urls import path, include
from FoodIndex_new import views
from FoodIndex_new.views import *
from django.conf.urls.static import static
from django.conf import settings
from home_app_new import views as hviews
from basic_app_new import views as bviews
app_name='FoodIndex_new'
urlpatterns = [
    path('upload_csv', views.upload_csv, name='upload_csv'),    
    path('filetodb', views.file_to_db, name='filetodb'),
    path('addfood', views.addfood, name='addfood'),
    path('getdata', views.getdata, name='getdata'),
    path('admin_login', views.login, name='login'),
    path('admin_signup', views.signup, name='signup'),
    path('alreadyuser', views.abc, name='alreadyuser'),
    path('base_table', views.base_table, name='base_table'),
    path('upload_csv_', views.xyz, name='upload_csv_'),
    path('user_signup', views.user_signup, name='user_signup'),
    path('user_signup_', views.createnewuser, name='user_signup'),
    path('home', hviews.home, name='home'),
    path('north', bviews.north, name='north'),
    path('table', hviews.table, name='table'),
    path('purchase', hviews.purchase, name='purchase'),
    path('', views.user_login, name='user_login'),
    path('profile_page',hviews.profile_page,name='profile_page'),
    path('search',bviews.search,name='search'),
    path('delete/<str:food_id>',views.delete_book,name="delete"),
    #path('chart',hviews.chart,name='chart'),
	#path('calchartthree',hviews.calchartthree,name='calchartthree'),
    path('update/<str:food_id>', views.update_food, name='update'),
    path('delete_table', views.delete_table, name='delete_table'),
    path('home/userfoodlogchart', hviews.userfoodlogchart, name='userfoodlogchart'),
    path('nut/', hviews.HomeView.as_view(),name='nut'),
    path('api', hviews.ChartData.as_view(),name='api'),
    path('chartof',hviews.chartof,name='chartof')

    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_URL)

