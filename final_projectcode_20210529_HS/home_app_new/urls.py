from django.urls import path,include
from home_app_new import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
app_name='home_app_new'


urlpatterns=[
	path('home/',views.home,name='home'),
	#path('renderhome/',views.renderhome, name='renderhome'),
	path('details/<str:f_name>/', views.details, name='details'),
    path('add_item1/', views.add_item1, name='add_item1'),
	path('delete/<str:f_name>/', views.delete, name='delete'),
	path('delete_purchase/<str:f_id>/', views.delete_purchase, name='delete_purchase'),
	path('table/', views.table, name='table'),
	path('purchase/', views.purchase, name='purchase'),
	path('confirm_purchase/', views.confirm_purchase, name='confirm_purchase'),
	path('confirm_purchase2/', views.confirm_purchase2, name='confirm_purchase2'),
	path('save_table/', views.save_table, name='save_table'),
	path('save_purchase/', views.save_purchase, name='save_purchase'),
	path('deletetemp/',views.deletetemp, name='deletetemp'),
	
	path('foodtopan',views.foodtopan,name='foodtopan'),
    path('profile_page/',views.profile_page,name='profile_page'),
	path('nut/', views.HomeView.as_view(),name='nut'),
    path('api', views.ChartData.as_view(),name='api'),
    path('chartof',views.chartof,name='chartof'),
	path('purchase_status',views.purchase_status,name='purchase_status'),
	path('consumed_history',views.consumer_history,name='consumed_history'),
	path('purchasechart', views.purchasechart, name='purchasechart'),
	path('otherdayanalysis', views.otherdayanalysis, name='otherdayanalysis'),



]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)